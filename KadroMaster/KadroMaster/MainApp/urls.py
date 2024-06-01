from django.urls import path
from MainApp.views import *

urlpatterns = [
    path('', profile_view, name="profile"),
]