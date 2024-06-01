from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from MainApp.forms import *
from MainApp.models import *

@login_required
def profile_view(request):
    return render(request, 'MainApp/main.html')
