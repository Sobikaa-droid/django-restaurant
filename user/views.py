from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView

from .forms import NewUserForm
from cart.models import Cart


class RegisterUserView(FormView):
    form_class = NewUserForm
    success_url = reverse_lazy('home')
    template_name = 'user/register.html'

    def form_valid(self, form):
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)

        self.request.session['cart_total'] = Cart.objects.filter(user=self.request.user).count()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)


class LoginUserView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')
    template_name = 'user/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())

        self.request.session['cart_total'] = Cart.objects.filter(user=self.request.user).count()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('home')
