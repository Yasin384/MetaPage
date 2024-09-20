from django.urls import path
from . import views

app_name = 'student_management'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance_report/', views.download_attendance_report, name='attendance_report'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('api/attendance/', views.AttendanceView.as_view(), name='attendance'),
    path('api/points/', views.PointsView.as_view(), name='points'),
    path('download_users_report/', views.download_users_report, name='download_users_report'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.login_view, name='login'),  # Add this line for the login view
]
