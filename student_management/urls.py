from django.urls import path
from . import views
app_name = 'student_management'
urlpatterns = [
    # ...
    path('api/attendance/', views.AttendanceView.as_view()),
    path('api/points/', views.PointsView.as_view()),
    path('check_attendance/', views.check_attendance, name='check_attendance'),

    # ...
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('download_attendance_report/', views.download_attendance_report, name='download_attendance_report'),
    path('download_users_report/', views.download_users_report, name='download_users_report'),
]
