'''Solutions. urls.py describes all of the mappings that we will
use for the application.
'''

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), # index: localhost:8000/app
    path('new', views.new, name='new'), # new: localhost:8000/app/new
    path('new_submit', views.new_submit, name='new_submit'),
    path('course_create', views.course_create, name='course_create'), # course_create: localhost:8000/course_create
    path('course_create_submit', views.course_create_submit, name='course_create_submit'),
    path('qr_create', views.qr_create, name='qr_create'), # qr_create: localhost:8000/qr_create
    path('qr_create_submit', views.qr_create_submit, name='qr_create_submit'),
    path('qr_upload', views.qr_upload, name='qr_upload'), # qr_upload: localhost:8000/qr_upload
    path('qr_upload_submit', views.qr_upload_submit, name='qr_upload_submit'),
]
