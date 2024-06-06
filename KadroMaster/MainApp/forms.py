from django import forms
from django.forms import ModelForm
from MainApp.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class AddDepartment(ModelForm):
    class Meta:
        model = Departments
        fields = ['title']

class AddJob(ModelForm):
    class Meta:
        model = Jobs
        fields = ['title', 'departament_title', 'salary_per_hour']

class AddUser(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'gender', 'birthday', 'residence_address', 'phone', 'employment_date', 'passport', 'email',
                  'individual_tax_number', 'insurance_number', 'work_book_number', 'job_title']

class AddTime(ModelForm):
    class Meta:
        model = TimeTraking
        fields = ['user', 'amount', 'date']