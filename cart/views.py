from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.core.paginator import Paginator

from menu.models import Food
from orders.models import Order
from .models import Cart
from .forms import AmountForm, CheckoutForm


class CartView(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.select_related('menu').filter(user=self.request.user)
        form = AmountForm()

        if cart.count() == 0:
            total_price = 0
            total_amount = 0
        else:
            total_price = float(cart.aggregate(Sum('price'))['price__sum'])
            total_amount = cart.aggregate(Sum('amount'))['amount__sum']

        paginator = Paginator(cart, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'total_price': total_price,
            'form': form,
        }

        self.request.session['cart_total'] = total_amount
        return render(self.request, 'cart/cart.html', context)


@login_required(login_url='user:register')
def add_to_cart(request, pk):
    """Adds or creates object of Menu to Cart with typed-in amount."""
    if request.method == 'POST':
        menu_object = get_object_or_404(Food, pk=pk)
        amount_to_add = int(request.POST.get('amount', 1))
        form = AmountForm(request.POST)
        if form.is_valid():
            try:
                Cart.objects.limit_check(amount_to_add=amount_to_add, user=request.user)
                Cart.objects.stock_check(menu_object=menu_object, amount_to_add=amount_to_add, user=request.user)
                if Cart.objects.filter(menu__name=menu_object.name, user=request.user).exists():
                    cart_object = get_object_or_404(Cart, menu__name=menu_object.name, user=request.user)
                    cart_object.price += (cart_object.price / cart_object.amount) * amount_to_add
                    cart_object.amount += amount_to_add
                    cart_object.save()
                else:
                    Cart.objects.create(
                        menu=menu_object,
                        price=menu_object.price * amount_to_add,
                        user=request.user,
                        amount=amount_to_add,
                    )

                cart_total = Cart.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']
                request.session['cart_total'] = cart_total
                messages.success(request, f'{menu_object.name} ({amount_to_add}) has been added to cart')

            except ValueError as error_message:
                messages.error(request, error_message)

        messages.error(request, form.errors)
        return redirect(request.META.get('HTTP_REFERER'))  # redirect to the same page


@login_required(login_url='user:register')
def update_all_objects(request):
    """Updates amounts and prices for EVERY object in cart."""
    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            input_amounts = [int(i) for i in request.POST.getlist('amount', None)]
            x = 0
            try:
                Cart.objects.limit_check(input_amounts=input_amounts, user=request.user)
                for input_number in input_amounts:
                    cart_object_name = Cart.objects.filter(user=request.user)[x]
                    cart_object = get_object_or_404(Cart, menu__name=cart_object_name, user=request.user)
                    if input_number <= cart_object.menu.stock and input_number != cart_object.amount:
                        cart_object.price = cart_object.price / cart_object.amount * input_number
                        cart_object.amount = input_number
                        cart_object.save()
                    x += 1
                messages.success(request, 'Cart has been updated')

            except ValueError as error_message:
                messages.error(request, error_message)

        messages.error(request, form.errors)
        return redirect('cart:cart')


@login_required(login_url='user:register')
def delete_from_cart(request, pk):
    if request.method == 'POST':
        cart_object = Cart.objects.select_related('menu').get(pk=pk, user=request.user)
        cart_object.delete()

        messages.success(request, f'{cart_object.menu.name} successfully deleted')
        return redirect('cart:cart')


@login_required(login_url='user:register')
def clear_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user)
        cart.delete()

        messages.success(request, 'Cart successfully cleared')
        return redirect('cart:cart')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.select_related('menu').filter(user=self.request.user)
        total_price = float(cart.aggregate(Sum('price'))['price__sum'])
        form = CheckoutForm()
        context = {
            'cart': cart,
            'total_price': total_price,
            'form': form,
        }
        return render(self.request, 'cart/checkout.html', context)

    def post(self, *args, **kwargs):
        """
        1. Gets all data for Order table.
        2. Creates Order table.
        3. Decreases stock value of menu objects and clears cart.
        """
        cart = Cart.objects.select_related('menu').filter(user=self.request.user)

        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            # 1
            products = {}
            for cart_object in cart:
                object_info = {
                    cart_object.menu.name: {
                        'image': cart_object.menu.image.url,
                        'amount': cart_object.amount,
                        'price': float(cart_object.price),
                    }
                }
                products.update(object_info)
            if form.cleaned_data['email'] == '':
                email_address = self.request.user.email
            else:
                email_address = form.cleaned_data['email']
            payment_type = form.cleaned_data['payment_type']
            total_amount = cart.aggregate(Sum('amount'))['amount__sum']
            total_price = cart.aggregate(Sum('price'))['price__sum']

            # 2
            Order.objects.create(
                products=products,
                email_address=email_address,
                payment_type=payment_type,
                total_amount=total_amount,
                total_price=total_price,
                user=self.request.user,
            )

            # 3
            for cart_object in cart:
                cart_object.menu.stock -= cart_object.amount
                cart_object.menu.save()
            cart.delete()

            context = {
                'email_address': email_address,
            }

            self.request.session['cart_total'] = 0
            messages.success(self.request, 'Successfull purchase!')
            return render(self.request, 'cart/checkout_success.html', context)
