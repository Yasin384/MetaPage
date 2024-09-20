from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    attended = models.BooleanField(default=False)

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses')