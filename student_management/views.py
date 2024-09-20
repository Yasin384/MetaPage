from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Attendance, Course
from django.utils import timezone
from geopy.distance import geodesic
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Attendance
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, User
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

def is_teacher(user):
    return user.is_authenticated and user.is_teacher

@user_passes_test(is_teacher)
def download_attendance_report(request):
    # ... (остальной код)

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        attendances = attendances.filter(date__range=[start_date, end_date])

    # ... (остальной код)

    return response

@user_passes_test(is_teacher)
def download_users_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Имя пользователя', 'Email', 'Баллы'])

    users = User.objects.all().order_by('username')
    for user in users:
        writer.writerow([user.username, user.email, user.points])

    return response
from django.db.models import Q

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

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = request.user in course.students.all()
    return render(request, 'course_detail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.students.all():
        course.students.add(request.user)
    return redirect('course_detail', course_id=course_id)

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user in course.students.all():
        course.students.remove(request.user)
    return redirect('course_detail', course_id=course_id)
class AttendanceView(APIView):
    def get(self, request):
        user = request.user
        attendance = Attendance.objects.filter(user=user)
        data = []
        for item in attendance:
            data.append({
                'date': item.date,
                'attended': item.attended,
            })
        return Response(data)

class PointsView(APIView):
    def get(self, request):
        user = request.user
        points = user.points
        return Response({'points': points})
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def check_attendance(request):
    user = request.user
    college_coords = (42.85756076410975, 74.59857798966878)
    user_coords = (request.POST.get('latitude'), request.POST.get('longitude'))
    
    distance = geodesic(college_coords, user_coords).meters
    
    if distance <= 150:
        Attendance.objects.create(user=user, date=timezone.now().date(), attended=True)
        user.points += 1
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Attendance marked'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not in the college area'})




@login_required
def leaderboard(request):
    users = User.objects.order_by('-points')
    paginator = Paginator(users, 20)  # 20 пользователей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'leaderboard.html', {'page_obj': page_obj})