from django.urls import path, include
from . import views

app_name = 'student_management'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('register/student/', views.register_student, name='register_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('attendance/check/', views.check_attendance, name='check_attendance'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('attendance/download/report/', views.download_attendance_report, name='download_attendance_report'),
    path('users/download/report/', views.download_users_report, name='download_users_report'),
]

