from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', login_required(views.OrdersView.as_view(), login_url='user:register'), name='orders'),
]