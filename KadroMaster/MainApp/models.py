from django.contrib.auth.models import AbstractUser
from django.db import models
import random, string

class Departments(models.Model):
    title = models.CharField(max_length=150, null=True, unique=True)
    amount = models.IntegerField(null=True, default=0)
    password = models.CharField(max_length=150, null=True)

class Jobs(models.Model):
    title = models.CharField(max_length=150, null=True)
    salary_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(null=True, default=0)
    departament_title = models.ForeignKey(Departments, on_delete=models.DO_NOTHING)

class User(AbstractUser):
    password = models.CharField(("password"), max_length=128, null=True)
    username = models.CharField(max_length=150, null=True, unique=True)
    gender = models.CharField(max_length=20, null=True)
    birthday = models.CharField(max_length=20, null=True)
    residence_address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    employment_date = models.CharField(max_length=16, null=True)
    passport = models.CharField(max_length=10, null=True)
    individual_tax_number = models.CharField(max_length=12, null=True)
    insurance_number = models.CharField(max_length=11, null=True)
    work_book_number = models.CharField(max_length=7, null=True)
    military_ticket = models.CharField(max_length=7, null=True)
    personnel_number = models.CharField(max_length=6, unique=True, null=True)
    password_kadr = models.CharField(max_length=150, null=True)
    job_title = models.ForeignKey(Jobs, on_delete=models.DO_NOTHING, null=True)
    access_lvl = models.CharField(max_length=255, null=True)

class TimeTraking(models.Model):
    date = models.CharField(max_length=20, null=True)
    amount = models.IntegerField()
    department = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Salary(models.Model):
    salary_date = models.CharField(max_length=20, null=True)
    number_of_hours_worked = models.CharField(max_length=20, null=True)
    final_salary = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

