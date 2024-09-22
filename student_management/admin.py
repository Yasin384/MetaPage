from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Teacher, Student, Course, Attendance, Enrollment

class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_teacher', 'course', 'faculty')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('is_teacher', 'course', 'faculty')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('is_teacher', 'course', 'faculty')}),
    )

# Регистрация кастомного администратора для модели User
admin.site.register(User, CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Enrollment)

