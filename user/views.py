from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import NewUserForm
from cart.models import Cart


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            request.session['cart_total'] = Cart.objects.filter(user=request.user).count()
            return redirect('home')

        messages.error(request, form.errors)

    form = NewUserForm(request.POST)
    return render(request, template_name="user/register.html", context={"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                request.session['cart_total'] = Cart.objects.filter(user=request.user).count()
                return redirect('home')

        messages.error(request, form.errors)

    form = AuthenticationForm(request.POST)
    return render(request, template_name="user/login.html", context={"form": form})


@login_required(login_url='user:register')
def logout_user(request):

    logout(request)
    return redirect('home')
