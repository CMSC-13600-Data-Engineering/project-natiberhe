'''Solutions. Now that you have worked through the application yourself
and know how data moves around, we have released a working prototype of 
the AttendanceChimp app that you can modify for HW5.
'''

# we are going to install some libraries for image processing
# to set it up locally
# pip install numpy opencv-python pillow
import cv2
import numpy as np
from PIL import Image

# these are django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
# these are import from your model
from .models import *
<<<<<<< HEAD
import time
=======
from django.contrib.auth.models import User
from .models import UniversityPerson
import time
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.contrib import messages



>>>>>>> 35d50855cb108c78ed0938823f6c660e142bece3


# below are all of the http "GET" requests
# note that these functions just create the pages
# they don't handle any data!
@csrf_exempt
def index(request):
<<<<<<< HEAD
    '''Presents the main landing page.

       Error checking: this view only triggers on a GET request.
    '''

    if request.method == "GET":
        return render(request, 'app/index.html', {})

    raise PermissionDenied

@csrf_exempt
def new(request):
    '''The page for creating a new user
       
       Error checking: 
            - this view only triggers on a GET request.
            - this view only triggers if the user isn't logged in
    '''

    # only go to this page if not logged in
    if request.method == "GET" and not request.user.is_authenticated:
        return render(request, 'app/new.html', {})
=======
    if request.method == "GET":
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current time
        return render(request, 'app/index.html', {'current_time': current_time})
    
@csrf_exempt
def handle_form(request):
    cname = request.POST['cname']
    cnum =  request.POST['cnum']
>>>>>>> 35d50855cb108c78ed0938823f6c660e142bece3

    raise PermissionDenied


@csrf_exempt
def course_create(request):
    '''The page for creating a new course
       
       Error checking: 
            - this view only triggers on a GET request.
            - this view fails if the user isn't logged in
            - view fails if the linkage between UniversityPerson and User breaks
    '''

    # don't allow not logged in users to do this
    if not request.user.is_authenticated or request.method == "POST":
        raise PermissionDenied

    # get the logged in user
    up = UniversityPerson.objects.filter(user_id = request.user.id)

    # fatal error
    if len(up) == 0:
        raise PermissionDenied

    up = up[0]

    return render(request, 'app/course_create.html', {'is_student': not up.is_instructor})


@csrf_exempt
def qr_create(request):
    '''The page for creating a QR code
       
       Error checking: 
            - this view only triggers on a GET request.
            - this view fails if the user isn't logged in
            - view fails if the linkage between UniversityPerson and User breaks
    '''
    if not request.user.is_authenticated or request.method == "POST":
        raise PermissionDenied

    # get the logged in user
    up = UniversityPerson.objects.filter(user_id = request.user.id)

    # fatal error
    if len(up) == 0:
        raise PermissionDenied

    up = up[0]
    courses = Course.objects.filter(instructor=up)

    return render(request, 'app/qr_create.html', {'courses': courses, 'is_student': not up.is_instructor})


@csrf_exempt
def qr_upload(request, errors=""):
    '''The page for uploading a QR code
       
       Error checking: 
            - this view fails if the user isn't logged in
            - view fails if the linkage between UniversityPerson and User breaks
    '''

    if not request.user.is_authenticated:
        raise PermissionDenied

    # get the logged in user
    up = UniversityPerson.objects.filter(user_id = request.user.id)

    # fatal error
    if len(up) == 0:
        raise PermissionDenied

    up = up[0]

    return render(request, 'app/qr_upload.html', {'is_student': not up.is_instructor, 'errors': errors})


# below are the functions that handle POST requests
# they are all named xyz_submit to handle it

@csrf_exempt
def new_submit(request):
    ''' Handles a submission from a new user creation form.
        
        Error Checking:
            - Raises an error if logged in
    '''

    # is a user logged in, if so fail
    if request.user.is_authenticated:
        raise PermissionDenied

    # get the post data
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    is_instructor = (request.POST.get("choice") == "instructor")

    # return back if there is some kind of an error
    if username is None or\
       email is None or\
       password is None or\
       request.POST.get("choice") is None:
       return render(request, 'app/new.html', {})

    # create and login
    user, _ = create_ac_user(username, email, password, is_instructor)
    login(request, user)

    # return to index
    return render(request, 'app/index.html', {})


@csrf_exempt
def course_create_submit(request):
    ''' Handles a submission from a new course creation form.

        Error Checking:
            - Raises an error if not logged in
    '''

    # is a user logged in
    if not request.user.is_authenticated:
        raise PermissionDenied

    # get the data
    name = request.POST.get("course-name")
    start_time = request.POST.get("start-time")
    end_time = request.POST.get("end-time")

    # if data is missing go baack
    if name is None or start_time is None or end_time is None:
        return render(request, 'app/course_create.html', {})

    # get the instructor
    instructor = UniversityPerson.objects.filter(user_id = request.user.id)

    # fatal error
    if len(instructor) == 0:
        raise PermissionDenied

    # not an instructor
    if not instructor[0].is_instructor:
        raise PermissionDenied

    instructor = instructor[0]

    # populate the days
    days = []
    if request.POST.get("day-mon"):
        days.append('M')

    if request.POST.get("day-tue"):
        days.append('Tu')

    if request.POST.get("day-wed"):
        days.append('W')

    if request.POST.get("day-thu"):
        days.append('Th')

    if request.POST.get("day-fri"):
        days.append('F')

    # create the course and go back home!
    create_course(name, instructor, days, start_time, end_time)
    return render(request, 'app/index.html', {})


@csrf_exempt
def qr_create_submit(request):
    ''' Handles a submission from a qr code creation form.

        Error Checking:
            - Raises an error if not logged in
    '''

    # is a user logged in
    if not request.user.is_authenticated:
        raise PermissionDenied

    course_id = request.POST.get("choice")

    # is the course id there
    if course_id is None:
        raise PermissionDenied

    # get the course object
    course = Course.objects.filter(auto_increment_id = course_id)
    if len(course) == 0:
        raise PermissionDenied

    # create and display
    course = course[0]
    code = create_qr_code(course)
    return render(request, 'app/qr_display.html', {'qrcode': code})


@csrf_exempt
def qr_upload_submit(request):
    ''' Handles a qr code upload.

        Error Checking:
            - Raises an error if not logged in
            - Raises error if not a student
    '''

    # must be logged in
    if not request.user.is_authenticated:
        raise PermissionDenied

    # must have a valid UP
    student = UniversityPerson.objects.filter(user_id = request.user.id)
    if len(student) == 0:
        raise PermissionDenied

    # must be a student
    student = student[0]
    if student.is_instructor:
        raise PermissionDenied

    # get the data
    file = request.FILES['imageUpload']

    # image processing
    img = Image.open(file) # load bytes as PIL image
    cv2img = np.array(img) # load into opencv

    # process image
    qcd = cv2.QRCodeDetector() 
    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(cv2img)

    if len(decoded_info) == 0:
        return qr_upload(request, "Cannot find a qr code")

    code = decoded_info[0].strip()
    
    # query QR code
    created_obj = QRCode.objects.filter(code = code)

    # if the image doesn't register as a QR code
    if len(created_obj) == 0:
        raise PermissionDenied

    created_obj = created_obj[0]

    process_upload(created_obj.course, student, file) 

    return render(request, 'app/index.html', {})

<<<<<<< HEAD

from django.http import JsonResponse
from .models import getUploadsForCourse

def getUploads(request):
    course_id = request.GET.get('course')
    if not course_id:
        return JsonResponse({'error': 'Course ID is required'}, status=400)
    
    try:
        course_id = int(course_id)
        uploads = getUploadsForCourse(course_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid course ID'}, status=400)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

    uploads_data = [
        {'username': upload.student.user.username, 'upload_time_as_string': upload.uploaded.strftime('%Y-%m-%d %H:%M:%S')}
        for upload in uploads
    ]

    return JsonResponse(uploads_data, safe=False)

from django.http import JsonResponse
from .models import getUploadsForCourse, Course

def getUploads(request):
    # Step 1: Check if there is a URL argument "course"
    course_id = request.GET.get('course')
    
    # Step 2: If course ID is missing, return an error
    if not course_id:
        return JsonResponse({'error': 'Course ID is required'}, status=400)
    
    try:
        # Convert course_id to integer and fetch uploads
        course_id = int(course_id)
        uploads = getUploadsForCourse(course_id)
    except ValueError:
        # Handle case where course_id is not an integer
        return JsonResponse({'error': 'Invalid course ID'}, status=400)
    except Course.DoesNotExist:
        # Handle case where no course matches the given ID
        return JsonResponse({'error': 'Course not found'}, status=404)

    # Step 3: Format the uploads into the specified structure
    uploads_data = [
        {'username': upload.student.user.username, 'upload_time_as_string': upload.uploaded.strftime('%Y-%m-%d %H:%M:%S')}
        for upload in uploads
    ]

    # Step 4: Return the serialized uploads data as JSON response
    return JsonResponse(uploads_data, safe=False)

=======
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
>>>>>>> 35d50855cb108c78ed0938823f6c660e142bece3
