from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('', views.get_courses, name='get-courses'),
    path('create-course/<str:pk>/', views.create_course, name='create-course'),
    path('get-course/<str:pk>/', views.get_course, name='get-course'),
    path('update-course/<str:pk>/', views.update_course, name='update-course'),
    path('delete-course/<str:pk>/', views.delete_course, name='delete-course'),
]
