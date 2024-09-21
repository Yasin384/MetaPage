from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Teacher, Student, Course, Attendance, Enrollment
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_teacher', 'course', 'faculty')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_teacher', 'course', 'faculty')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_teacher', 'course', 'faculty')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Enrollment)