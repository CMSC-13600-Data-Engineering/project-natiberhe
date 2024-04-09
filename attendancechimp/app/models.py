from django.db import models

# Create your models here.
class Student(models.Model):
    studname = models.CharField(max_length=70, null = False)
    studentid = models.IntegerField(primary_key = True)
    def __str__(self):
        return self.name
class Instructor(models.Model):
    instname = models.CharField(max_length=256,null = False)
    instid = models.IntegerField(primary_key = True)
    def __str__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=256, primary_key=True)
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.title
    
class Attendance(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecture_date = models.DateField()

    def __str__(self):
        return self.title

class QRCode(models.Model):
    qr_code_id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/')
    is_valid = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
