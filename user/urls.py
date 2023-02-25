from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('log-in', views.login_user, name='login'),
    path('log-out', views.logout_user, name='logout'),
]
