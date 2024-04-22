from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.models import User
from .models import UniversityPerson
import time
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib import messages




@csrf_exempt
def index(request):
    if request.method == "GET":
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current time
        return render(request, 'app/index.html', {'current_time': current_time})
    
@csrf_exempt
def handle_form(request):
    cname = request.POST['cname']
    cnum =  request.POST['cnum']

    print(cname, cnum)

    new_course = Course(cname, cnum)
    new_course.save()

    return render(request, 'app/index.html', {})

def new(request):
    if request.method == 'GET' and not request.user.is_authenticated:
        return render(request, 'app/new.html')
    return PermissionDenied

def create_ac_user(name, email, password, is_instructor):
    user = User.objects.create_user(username=name, email=email, password=password)
    user.save()

    np = UniversityPerson.objects.create(user=user, is_instructor=is_instructor)
    np.save()

    return user, np

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_instructor = (request.POST.get("choice") == "instructor")

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return render(request, 'app/new.html',{'error': 'Email already in use'})

        user, np = create_ac_user(username, email, password, is_instructor)
        user.save()
        login(request, user)
        
        messages.success(request, 'User created successfully!')
        return redirect('index')
                
    else:
        return render(request, 'app/new.html', {'error':'invalid request'})