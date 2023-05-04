from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', login_required(views.CartView.as_view(), login_url='user:register'), name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add'),
    path('update/', views.update_all_objects, name='update_all'),
    path('delete/<int:pk>/', views.delete_from_cart, name='delete'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('checkout/', login_required(views.CheckoutView.as_view(), login_url='user:register'), name='checkout'),
]
