'''SOLUTIONS. These are solutions that might help you think about
the problem in a different way. Note the simplicity of the models
compared to some of what you might have implemented. We'll walk 
through all of this step-by-step. 
'''

# import to get the models class  from django
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class UniversityPerson(models.Model):
    """This model describes a university person, either a student
    or an instructor. It contains all of the necessary data that
    might identify such a person.

    Note: We link this entity to the Django user model so we only
    need to store information unique to a "UniversityPerson" above
    and beyond a simple user.
    """

    # an auto incrementing id
    auto_increment_id = models.AutoField(primary_key=True)

    # is an instructor or student?
    is_instructor = models.BooleanField(null=False)

    # relate to django auth user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# for each model, I like to wrap it in a simple helper function
# for example for the user model, when creating a user we create
# two users one university person and one django user.
def create_ac_user(name, email, password, is_instructor):
    """Creates an ac user and a corresponding django user"""

    # first create django user
    user = User.objects.create_user(name, email, password)
    user.save()

    # then create ac user
    up = UniversityPerson(is_instructor=is_instructor, user=user)
    up.save()

    # return both users
    return user, up


# get access to django users
from django.contrib.auth.models import User

# some stuff to get the QR code working easier
from django.utils.crypto import get_random_string


class UniversityPerson(models.Model):
    """This model describes a university person, either a student
    or an instructor. It contains all of the necessary data that
    might identify such a person.

    Note: We link this entity to the Django user model so we only
    need to store information unique to a "UniversityPerson" above
    and beyond a simple user.
    """

    # an auto incrementing id
    auto_increment_id = models.AutoField(primary_key=True)

    # is an instructor or student?
    is_instructor = models.BooleanField(null=False)

    # relate to django auth user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# for each model, I like to wrap it in a simple helper function
# for example for the user model, when creating a user we create
# two users one university person and one django user.
def create_ac_user(name, email, password, is_instructor):
    """Creates an ac user and a corresponding django user"""

    # first create django user
    user = User.objects.create_user(name, email, password)
    user.save()

    # then create ac user
    up = UniversityPerson(is_instructor=is_instructor, user=user)
    up.save()

    # return both users
    return user, up


class Course(models.Model):
    """A course represents a single course using attendancechimp. A course
    stores a reference to the instructor as well as the times/days of the
    week that it meets."""

    # an internal unique id
    auto_increment_id = models.AutoField(primary_key=True)

    # a course name
    name = models.CharField(max_length=128)

    # foreign key to instructor
    instructor = models.ForeignKey(UniversityPerson, on_delete=models.CASCADE)

    # class time start and end
    class_start = models.TimeField()
    class_end = models.TimeField()

    # class days
    m_class = models.BooleanField(default=False)
    tu_class = models.BooleanField(default=False)
    w_class = models.BooleanField(default=False)
    th_class = models.BooleanField(default=False)
    f_class = models.BooleanField(default=False)


# let's spec out the basic functionality of a course
def create_course(name, instructor, days, start, end):
    """Creates an ac user and a corresponding django user"""
    course = Course(name=name, instructor=instructor, class_start=start, class_end=end)

    # handles course meetings
    for d in days:
        if d == "M":
            course.m_class = True

        if d == "Tu":
            course.tu_class = True

        if d == "W":
            course.w_class = True

        if d == "Th":
            course.th_class = True

        if d == "F":
            course.f_class = True

    course.save()

    return course


class QRCode(models.Model):
    """A qr code is tied to a particular lecture. Note this object just defines the
    QR code does not contain any image data.
    """

    # an internal unique id
    auto_increment_id = models.AutoField(primary_key=True)

    # linked to a course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # code
    code = models.CharField(max_length=32)

    # this is a trick to automatically generate a random
    # string on save
    def save(self, *args, **kwargs):
        self.code = get_random_string(length=32)
        super(QRCode, self).save(*args, **kwargs)


# this is the functionality to create a qr code
def create_qr_code(course):
    qrcode = QRCode(course=course)
    qrcode.save()
    return qrcode


class QRCodeUpload(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the ID field, though it's usually not necessary
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(UniversityPerson, on_delete=models.CASCADE)
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)



# this is the functionality to process an upload
def process_upload(course, student, qr_code, image=None):
    upload = QRCodeUpload(course=course, student=student, qr_code=qr_code, image=image)
    upload.save()
    return upload


import datetime
from django.utils import timezone
import pytz

def getUploadsForCourse(course_id):
    try:
        course = Course.objects.get(auto_increment_id=course_id)
    except Course.DoesNotExist:
        return []

    uploads = QRCodeUpload.objects.filter(course=course)
    valid_uploads = []
    central_tz = pytz.timezone('America/Chicago')  # Ensure timezone awareness

    day_mapping = {
        0: course.m_class,  # Monday
        1: course.tu_class, # Tuesday
        2: course.w_class,  # Wednesday
        3: course.th_class, # Thursday
        4: course.f_class   # Friday
    }

    for upload in uploads:
        # Convert the uploaded time to Central Time Zone
        upload_dt = upload.uploaded.astimezone(central_tz)
        upload_day = upload_dt.weekday()
        upload_time = upload_dt.time()
        
        # Combine date and time with proper timezone
        start_datetime = central_tz.localize(datetime.datetime.combine(upload_dt.date(), course.class_start))
        end_datetime = central_tz.localize(datetime.datetime.combine(upload_dt.date(), course.class_end))

        print(f"Day Mapping: {day_mapping}")
        print(f"Upload Day: {upload_day}, Mapped Value: {day_mapping.get(upload_day, False)}")
        print(f"Upload Time: {upload_time}, Course Time Range: {start_datetime} {end_datetime}")
        
        if day_mapping.get(upload_day, False) and (start_datetime <= upload_dt <= end_datetime):
            valid_uploads.append(upload)

    return valid_uploads
