from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register),
    path('get-user/', views.get_user),
    path('logout/', views.BlacklistTokenUpdateView.as_view()),
    path('edit-user/', views.edit_user),
    path("change-password/<int:pk>/", views.ChangePasswordView.as_view())
]
