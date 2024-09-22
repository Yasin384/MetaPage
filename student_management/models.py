from django.db import models
from django.contrib.auth.models import AbstractUser

# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    course = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], null=True, blank=True)
    faculty = models.CharField(max_length=10, choices=[
        ('КБ', 'КБ'),
        ('БЧ', 'БЧ'),
        ('ИЯ', 'ИЯ'),
        ('КвПС', 'КвПС'),
        ('ИИ', 'ИИ'),
        ('РИ', 'РИ')
    ], null=True, blank=True)

    def __str__(self):
        return f"{self.username}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Добавьте дополнительные поля для учителя, если необходимо

    def __str__(self):
        return f"{self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Добавьте дополнительные поля для студента, если необходимо

    def __str__(self):
        return f"{self.user.username}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} on {self.date}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses')

    def __str__(self):
        return f"{self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # Note the 'Course' string 
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"
