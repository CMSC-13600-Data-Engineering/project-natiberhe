from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    #path('handleform', views.handle_form, name='form'),
    path('app/new', views.new, name='new'),
    path('app/create_user', views.create_user, name='create_user'),
]
