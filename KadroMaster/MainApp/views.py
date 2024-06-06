from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from MainApp.forms import *
from MainApp.models import *
from django.db.models import F, Q, Sum
import datetime

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def profile_view(request, id = None, job_title = None):
    employeers = User.objects.filter(job_title__isnull=False)
    if request.method == 'GET':
        if request.user.is_authenticated:
            if id is not None:
                User.objects.filter(id=id).delete()
                Jobs.objects.filter(id=job_title).update(amount=F("amount") - 1)
                Departments.objects.filter(id=Jobs.objects.filter(id=job_title)[0].departament_title.id).update(amount=F("amount") - 1)
                return redirect("profile")
            return render(request, "MainApp/main.html", {'employeers': employeers})
        else:
            return redirect("login")
    return render(request, 'MainApp/main.html', {'employeers': employeers})

def auth(request):
    if request.user.is_authenticated:
        return redirect('main')

    users = User.objects.filter(password__isnull=False, access_lvl__isnull=False)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
            else:
                error_message = "Неправильный пароль!"
                return render(request, 'MainApp/login.html', {'form': form, 'error_message': error_message, 'users': users})
    else:
        form = LoginForm()
    return render(request, 'MainApp/login.html', {'form': form, 'users': users})

def add_department(request, title = None, amount = None):
    departments = Departments.objects.all()
    if request.method == 'GET':
        if request.user.is_authenticated:
            if amount == '0':
                print(Departments.objects.all().filter(title=title)[0].id)
                id_dep = Departments.objects.all().filter(title=title)[0].id
                Jobs.objects.filter(departament_title=id_dep).delete()
                Departments.objects.filter(title=title).delete()

                #Jobs.objects.filter(departament_title=title).delete()
                return redirect("department")
            else:
                print('err')
            return render(request, 'MainApp/add_department.html', {'departments': departments})
        else:
            return redirect("login")

    if request.POST:
        form = AddDepartment(request.POST)
        if form.is_valid():
            db = form.save(commit=False)
            db.password = generate_random_string(8)
            db.save()

        else:
            print('err')
    return  render(request, 'MainApp/add_department.html', {'departments': departments})

def add_personal(request, id = None, department = 'Отдел', jobs = None):
    departments = Departments.objects.all()
    #print(Departments.objects.all().filter(id=29)[0].title)
    if id:
        department = Departments.objects.all().filter(id=id)[0].title
        jobs = Jobs.objects.filter(departament_title=id)

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "MainApp/add_personal.html", {'departments': departments, 'department': department, 'jobs': jobs, 'id': id})
        else:
            return redirect("login")

    if request.POST:
        form = AddUser(request.POST)
        if form.is_valid():
            db = form.save(commit=False)
            if request.POST['military_ticket']:
                db.military_ticket = request.POST['military_ticket']
            db.personnel_number = random.randint(100000,999999)
            db.save()
            Jobs.objects.filter(id=request.POST['job_title']).update(amount=F("amount") + 1)
            Departments.objects.filter(id=Jobs.objects.filter(id=request.POST['job_title'])[0].departament_title.id).update(amount=F("amount") + 1)
            #print(Jobs.objects.all().filter(title=request.POST['username']))
            print(request.POST['job_title'])
            print(Jobs.objects.all().filter(id=request.POST['job_title'])[0].departament_title.id)
            print(Departments.objects.all().filter(id=Jobs.objects.all().filter(id=request.POST['job_title'])[0].departament_title.id)[0].password)
            print(User.objects.get(username=request.POST['username']))


            if Jobs.objects.all().filter(id=request.POST['job_title'])[0].title == 'Руководитель отдела':
                db = User.objects.get(username=request.POST['username'])
                db.set_password(str(Departments.objects.all().filter(id=Jobs.objects.all().filter(id=request.POST['job_title'])[0].departament_title.id)[0].password))
                db.save()
                if Departments.objects.all().filter(id=id)[0].title == 'Отдел кадров':
                    User.objects.filter(username=request.POST['username']).update(access_lvl=1)
            elif Departments.objects.all().filter(id=id)[0].title == 'Отдел кадров':
                password = generate_random_string(12)
                db = User.objects.get(username=request.POST['username'])
                db.set_password(password)
                db.save()
                User.objects.filter(username=request.POST['username']).update(password_kadr=password)
                User.objects.filter(username=request.POST['username']).update(access_lvl=1)

        else:
            print('err')

    return render(request, 'MainApp/add_personal.html', {'departments': departments, 'department': department, 'jobs': jobs, 'id': id})

def add_job(request, title = None, amount = None):
    departments = Departments.objects.all()
    jobs = Jobs.objects.all()
    if request.method == 'GET':
        if request.user.is_authenticated:
            if amount == '0':
                Jobs.objects.filter(title=title).delete()
                return redirect("job")
            else:
                print('err')
            return render(request, "MainApp/add_job.html", {'departments': departments, 'jobs': jobs})
        else:
            return redirect("login")

    if request.POST:
        form = AddJob(request.POST)
        if form.is_valid():
            db = form.save(commit=False)
            db.save()
        else:
            print('err')
    return render(request, 'MainApp/add_job.html', {'departments': departments, 'jobs': jobs})

def info_personal(request, id = None, department_id = None):
    employeer = User.objects.filter(id=id)[0]
    departments = Departments.objects.all()
    department = employeer.job_title.departament_title
    jobs = None
    if department_id:
        department = Departments.objects.all().filter(id=department_id)[0]
        jobs = Jobs.objects.filter(departament_title=department_id)

    print(User.objects.filter(id=id)[0].job_title.id)

    #request.POST['military_ticket']
    if request.method == 'POST':
        print(User.objects.filter(id=id)[0].military_ticket == request.POST['military_ticket'])
        print(request.POST['military_ticket'])


        try:
            db = User.objects.filter(id=id)
            db.update(username=request.POST['username'])
            db.update(birthday=request.POST['birthday'])
            db.update(gender=request.POST['gender'])
            db.update(phone=request.POST['phone'])
            db.update(residence_address=request.POST['residence_address'])
            db.update(passport=request.POST['passport'])
            db.update(insurance_number=request.POST['insurance_number'])
            db.update(individual_tax_number=request.POST['individual_tax_number'])
            db.update(work_book_number=request.POST['work_book_number'])
            db.update(military_ticket=request.POST['military_ticket'])
            db.update(email=request.POST['email'])
            if User.objects.filter(id=id)[0].job_title != request.POST['job_title']:
                Jobs.objects.filter(id=User.objects.filter(id=id)[0].job_title.id).update(amount=F("amount") - 1)
                Departments.objects.filter(id=Jobs.objects.filter(id=User.objects.filter(id=id)[0].job_title.id)[0].departament_title.id).update(amount=F("amount") - 1)
                Jobs.objects.filter(id=request.POST['job_title']).update(amount=F("amount") + 1)
                Departments.objects.filter(
                    id=Jobs.objects.filter(id=request.POST['job_title'])[0].departament_title.id).update(
                    amount=F("amount") + 1)

                User.objects.filter(id=id).update(job_title=int(str(request.POST['job_title'])))
        except:
            print('err')
        return redirect("profile")

    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "MainApp/info_personal.html", {'employeer': employeer, 'departments': departments, 'jobs': jobs, 'department': department})
        else:
            return redirect("login")

def access_view(request):
    personnels = User.objects.all().filter(password__isnull=False, access_lvl__isnull=False).exclude(username='admin')
    print(personnels)
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "MainApp/access.html", {'personnels': personnels})
        else:
            return redirect("login")

def leader_auth(request):
    if request.user.is_authenticated:
        return redirect('main')

    users = User.objects.filter(password__isnull=False, access_lvl__isnull=True)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'leader')
                return redirect(next_url)
            else:
                error_message = "Неправильный пароль!"
                return render(request, 'MainApp/login.html', {'form': form, 'error_message': error_message, 'users': users})
    else:
        form = LoginForm()
    return render(request, 'MainApp/login.html', {'form': form, 'users': users})

def leader_view(request):
    #print(User.objects.all().filter(job_title=Jobs.objects.all().filter(departament_title=request.user.job_title.departament_title.id)[0]).values_list("id"))
    try:
        employees = User.objects.all().filter(job_title__in=Jobs.objects.all().filter(departament_title=request.user.job_title.departament_title.id))
        hours = TimeTraking.objects.all().filter(department=request.user.job_title.departament_title.id)
        print(employees)
        print(Jobs.objects.all().filter(departament_title=request.user.job_title.departament_title.id))
    except:
        print('Анлаки')
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "MainApp/leader.html", {'employees': employees, 'hours': hours})
        else:
            return redirect("leader_login")

    if request.POST:
        form = AddTime(request.POST)
        if form.is_valid():
            db = form.save(commit=False)
            db.department = request.user.job_title.departament_title
            db.save()
        else:
            print(form.errors)
    return render(request, "MainApp/leader.html", {'employees': employees, 'hours': hours})

def salary_view(request, id):
    username = User.objects.all().filter(id=id)[0]
    salaries = Salary.objects.all().filter(user=id)
    print(User.objects.filter(id=id))
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "MainApp/report_salary.html", {'username': username, 'salaries': salaries})
        else:
            return redirect("leader_login")
    if request.POST:
        if 'add' in request.POST:
            print(request.POST['from'])
            print(request.POST['before'])
            print(Jobs.objects.all().filter(id=username.job_title.id)[0].salary_per_hour)
            print(TimeTraking.objects.all().filter(user=id).aggregate(Sum('amount'))['amount__sum'])
            print(TimeTraking.objects.all().filter(user=id, date__range=(request.POST['from'], request.POST['before'])).aggregate(Sum('amount'))['amount__sum'])
            if request.POST['from'] > request.POST['before']:
                print('123')
            else:
                employee_salary_hour = Jobs.objects.all().filter(id=username.job_title.id)[0].salary_per_hour
                employee_amount_hours = TimeTraking.objects.all().filter(user=id, date__range=(request.POST['from'], request.POST['before'])).aggregate(Sum('amount'))['amount__sum']
                employee_final_salary = employee_salary_hour * employee_amount_hours
                print(employee_final_salary)
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                Salary.objects.create(salary_date=current_date, number_of_hours_worked=employee_amount_hours, final_salary=employee_final_salary, user=username)
            return render(request, "MainApp/report_salary.html", {'username': username, 'salaries': salaries})