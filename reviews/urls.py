from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('bootcamp/<str:pk>/', views.get_bootcamp_reviews,
         name="get-bootcamp-reviews"),
    path("get-review/<str:pk>/", views.get_review, name="get-review"),
    path("get-reviews-for-user/", views.get_reviews_for_user,
         name="get-reviews-for-user"),
    path('create-review/<str:pk>/', views.add_review, name="add-review"),
    path('update-review/<str:pk>/', views.update_review, name="update-review"),
    path('delete-review/<str:pk>/', views.delete_review, name="delete-review"),
]
