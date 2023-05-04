from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'user'

urlpatterns = [
    path('register', views.RegisterUserView.as_view(), name='register'),
    path('log-in', views.LoginUserView.as_view(), name='login'),
    path('log-out', login_required(views.LogoutUserView.as_view(), login_url='user:register'), name='logout'),
]
