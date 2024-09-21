from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from geopy.distance import geodesic
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
import csv

from .models import User, Attendance, Course, Teacher, Student, Enrollment
from .forms import TeacherSignUpForm, StudentSignUpForm, LoginForm

# Проверка: является ли пользователь преподавателем
def is_teacher(user: User) -> bool:
    return user.is_authenticated and user.is_teacher

# Логин
def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')  # Перенаправление на дашборд после входа
    return render(request, 'registration/login.html', {'form': form})

# Выход из системы
@login_required
def logout_view(request):
    logout(request)
    return redirect('student_management:home')  # Перенаправление на главную страницу

# Главная страница
def home(request):
    return render(request, 'base.html')

# Регистрация преподавателя
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration/register_teacher.html', {'form': form})

# Регистрация студента
def register_student(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/register_student.html', {'form': form})

# Дашборд
@login_required
def dashboard(request):
    user = request.user
    points = user.points
    attendance = Attendance.objects.filter(user=user)
    return render(request, 'dashboard.html', {'points': points, 'attendance': attendance})

# Список курсов с поиском
@login_required
def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(
            Q(name__icontains=query) | Q(teacher__username__icontains=query)
        )
    else:
        courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# Детали курса
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = request.user in course.students.all()
    return render(request, 'course_detail.html', {'course': course, 'is_enrolled': is_enrolled})

# Запись на курс
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.students.all():
        course.students.add(request.user)
    return redirect('course_detail', course_id=course_id)

# Отписка от курса
@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user in course.students.all():
        course.students.remove(request.user)
    return redirect('course_detail', course_id=course_id)

# Профиль преподавателя
@login_required
def teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = teacher.user.taught_courses.all()
    return render(request, 'teachers/teacher_profile.html', {'teacher': teacher, 'courses': courses})

# Создание курса
@login_required
def create_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        course = Course.objects.create(name=name, description=description, teacher=request.user)
        return redirect('teachers:teacher_profile')
    return render(request, 'teachers/create_course.html')

# Редактирование курса
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.teacher != request.user:
        return redirect('teachers:teacher_profile')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        course.name = name
        course.description = description
        course.save()
        return redirect('teachers:course_detail', course_id=course_id)
    return render(request, 'teachers/edit_course.html', {'course': course})

# Профиль студента
@login_required
def student_profile(request):
    student = Student.objects.get(user=request.user)
    courses = student.user.enrolled_courses.all()
    attendance = Attendance.objects.filter(user=request.user).order_by('-date')[:5]
    return render(request, 'students/student_profile.html', {'student': student, 'courses': courses, 'attendance': attendance})

# Отметка посещаемости с проверкой геолокации
@login_required
def check_attendance(request):
    user = request.user
    college_coords = (42.85756076410975, 74.59857798966878)

    try:
        user_coords = (
            float(request.POST.get('latitude')),
            float(request.POST.get('longitude'))
        )
        distance = geodesic(college_coords, user_coords).meters
    except (ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid coordinates'}, status=400)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Error calculating distance'}, status=500)
    
    if distance <= 150:
        Attendance.objects.create(user=user, date=timezone.now().date(), attended=True)
        user.points += 1
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Attendance marked'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not in the college area'})

# Лидерборд
@login_required
def leaderboard(request):
    users = User.objects.order_by('-points')
    paginator = Paginator(users, 20)  # 20 пользователей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'leaderboard.html', {'page_obj': page_obj})

# Скачивание отчета по посещаемости
@user_passes_test(is_teacher)
def download_attendance_report(request) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Username', 'Attended'])

    attendances = Attendance.objects.all().order_by('date')
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        attendances = attendances.filter(date__range=[start_date, end_date])

    for attendance in attendances:
        writer.writerow([attendance.date, attendance.user.username, attendance.attended])

    return response

# Скачивание отчета по пользователям
@user_passes_test(is_teacher)
def download_users_report(request) -> HttpResponse:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Points'])

    users = User.objects.all().order_by('username')
    for user in users:
        writer.writerow([user.username, user.email, user.points])

    return response

# Просмотр посещаемости (API)
class AttendanceView(APIView):
    def get(self, request) -> Response:
        user = request.user
        attendance = Attendance.objects.filter(user=user)
        data = [{'date': item.date, 'attended': item.attended} for item in attendance]
        return Response(data)

# Просмотр очков пользователя (API)
class PointsView(APIView):
    def get(self, request) -> Response:
        user = request.user
        points = user.points
        return Response({'points': points})
