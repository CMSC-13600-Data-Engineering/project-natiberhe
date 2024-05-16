import os
import django
from django.utils import timezone
import datetime
import time
import pytz
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendancechimp.settings")
django.setup()

from app.models import *

print("[1] Initializing Django successful")

# Clean up previous data
User.objects.all().delete()
print("[2] Deleted all users")

# Use timezone.now() to get the current time
current_datetime = timezone.now()
chicago_tz = pytz.timezone('America/Chicago')
local_datetime = current_datetime.astimezone(chicago_tz)
current_time = local_datetime.time()
end_time = (local_datetime + datetime.timedelta(minutes=1)).time()

# Create instructors and their courses
john_django, john_up = create_ac_user("John Doe", "johndoe@example.com", "password", True)
jane_django, jane_up = create_ac_user("Jane Bar", "janebar@example.com", "password", True)

john_course = create_course("Data Science 101", john_up, ['W'], current_time, end_time)
jane_course = create_course("AI Fundamentals", jane_up, ['W'], current_time, end_time)
print("[3] Courses created")
print(john_course.auto_increment_id)
print(jane_course.auto_increment_id)

# Create QR codes for each course
john_qr = create_qr_code(john_course)
jane_qr = create_qr_code(jane_course)
print("[4] QR codes created")

# Process uploads within the course time
for i in range(5):
    student_django, student_up = create_ac_user(f"StudentJohn{i}", f"studentjohn{i}@example.com", "password", False)
    process_upload(john_course, student_up, john_qr, None)  

for i in range(5):
    student_django, student_up = create_ac_user(f"StudentJane{i}", f"studentjane{i}@example.com", "password", False)
    process_upload(jane_course, student_up, jane_qr, None)  

print("Pausing for 60 seconds to simulate time passage...")
time.sleep(65)

# Process invalid uploads after the course time
for i in range(10, 20):
    student_django, student_up = create_ac_user(f"StudentLate{i}", f"studentlate{i}@example.com", "password", False)
    process_upload(john_course, student_up, john_qr, None)  # These uploads should be invalid due to time constraints

print("[5] Users QRCodeUploads processed")

# Assuming your Django development server is running

def get_uploads_df(course):
    response = pd.read_json(f'http://localhost:8000/app/getUploads?course={course.auto_increment_id}')
    response['upload_time_as_string'] = pd.to_datetime(response['upload_time_as_string'])
    response['upload_time_as_string'] = response['upload_time_as_string'].dt.tz_localize('UTC').dt.tz_convert('America/Chicago')
    response['upload_time_as_string'] = response['upload_time_as_string'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return response

df_john = get_uploads_df(john_course)
df_jane = get_uploads_df(jane_course)

print("John's Course Uploads:")
print(df_john)
print("\nJane's Course Uploads:")
print(df_jane)
print("[6] QRCodeUploads displayed")
