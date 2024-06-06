from django.urls import path
from MainApp.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', profile_view, name="profile"),
    path('login/', auth, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_department/', add_department, name='department'),
    path('add_department/<title>/<amount>/', add_department, name='department_del'),
    path('add_personal/', add_personal, name='personal'),
    path('add_job/', add_job, name='job'),
    path('add_job/<title>/<amount>/', add_job, name='job_del'),
    path('add_personal/<id>/', add_personal, name='personal_add'),
    path('del/<id>/<job_title>/', profile_view, name='profile_del'),
    path('info_personal/', info_personal, name='info'),
    path('info_personal/<id>/', info_personal, name='info_user'),
    path('info_personal/<id>/<department_id>/', info_personal, name='info_user_add'),
    path('access/', access_view, name='access'),
    path('leader/', leader_view, name='leader'),
    path('leader/login/', leader_auth, name='leader_login'),
    path('salary/<id>/', salary_view, name='salary'),
]