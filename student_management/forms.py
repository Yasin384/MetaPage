from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')  # Добавляем email и имя

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    course = forms.ChoiceField(choices=[(1, 'Курс 1'), (2, 'Курс 2'), (3, 'Курс 3')], required=True)
    faculty = forms.ChoiceField(choices=[('КБ', 'КБ'), ('БЧ', 'БЧ'), ('ИЯ', 'ИЯ'), ('КвПС', 'КвПС'), ('ИИ', 'ИИ'), ('РИ', 'РИ')], required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'course', 'faculty')  # Добавляем email и имя

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if course not in [1, 2, 3]:
            raise ValidationError("Выберите корректный курс.")
        return course

    def clean_faculty(self):
        faculty = self.cleaned_data.get('faculty')
        valid_faculties = ['КБ', 'БЧ', 'ИЯ', 'КвПС', 'ИИ', 'РИ']
        if faculty not in valid_faculties:
            raise ValidationError("Выберите корректный факультет.")
        return faculty

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'autofocus': True, 'autocomplete': 'username'}))
    password = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
