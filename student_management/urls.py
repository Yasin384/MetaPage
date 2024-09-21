from django.urls import path
from . import views

app_name = 'student_management'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register_teacher/', views.register_teacher, name='register_teacher'),
    path('register_student/', views.register_student, name='register_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('teachers/profile/', views.teacher_profile, name='teacher_profile'),
    path('teachers/create_course/', views.create_course, name='create_course'),
    path('teachers/course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('students/profile/', views.student_profile, name='student_profile'),
    path('attendance/check/', views.check_attendance, name='check_attendance'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('download_attendance_report/', views.download_attendance_report, name='download_attendance_report'),
    path('download_users_report/', views.download_users_report, name='download_users_report'),
    path('api/attendance/', views.AttendanceView.as_view(), name='attendance'),
    path('api/points/', views.PointsView.as_view(), name='points'),
    path('attendance_report/', views.download_attendance_report, name='attendance_report'),
]