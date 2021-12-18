from django.urls import path
from . import views

app_name = 'bootcamps'

urlpatterns = [
    path('', views.get_bootcamps, name="get-bootcamps"),
    path('get-latest-bootcamps/', views.get_latest_bootcamps),
    path('create-bootcamp/', views.create_bootcamp, name="create-bootcamp"),
    path('get-bootcamp/<str:pk>/', views.get_bootcamp, name="get-bootcamp"),
    path('get-bootcamp-for-user/',
         views.get_bootcamp_for_user, name="get-bootcamp-for-user"),
    path('update-bootcamp/<str:pk>/',
         views.update_bootcamp, name="update-bootcamp"),
    path('delete-bootcamp/<str:pk>/',
         views.delete_bootcamp, name="delete-bootcamp"),
    path('upload-photo/<str:pk>/', views.upload_photo, name="upload-photo"),
    path("get-bootcamps-within-radius/<int:km>/<str:zipcode>/",
         views.get_bootcamps_within_radius)
]
