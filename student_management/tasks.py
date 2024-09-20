
from celery import shared_task
from .models import User, Attendance
from celery import shared_task

from .models import User, Attendance
from geopy.distance import geodesic
from datetime import datetime, timedelta

@shared_task
def check_attendance():
    users = User.objects.all()
    college_coords = (42.85756076410975, 74.59857798966878)
    current_time = datetime.now()
    start_time = current_time.replace(hour=9, minute=0, second=0)
    end_time = current_time.replace(hour=10, minute=20, second=0)

    for user in users:
        user_coords = (user.latitude, user.longitude)
        distance = geodesic(college_coords, user_coords).meters

        if distance <= 150 and start_time <= current_time <= end_time:
            Attendance.objects.create(user=user, date=current_time.date(), attended=True)
            user.points += 1
            user.save()
        else:
            Attendance.objects.create(user=user, date=current_time.date(), attended=False)