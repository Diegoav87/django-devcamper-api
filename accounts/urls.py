from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register),
    path('get-user/', views.get_user),
    path('logout/', views.BlacklistTokenUpdateView.as_view())
]
