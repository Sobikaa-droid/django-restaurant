from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

from menu.models import Food


class CartManager(models.Manager):
    def limit_check(self, user, amount_to_add=None, input_amounts=None):
        qs = super().get_queryset().filter(user=user)

        limit_number = 50
        cart_amounts = [int(i.amount) for i in qs]

        if amount_to_add:
            if amount_to_add + sum(cart_amounts) > limit_number:
                raise ValueError(f"Amount value can not overcome cart's limit of {limit_number}.")
        if input_amounts:
            if sum(input_amounts) + sum(cart_amounts) - sum(cart_amounts) > limit_number:
                raise ValueError(f"Total amount value can not overcome cart's limit of {limit_number}.")

    def stock_check(self, user, menu_object, amount_to_add):
        qs = super().get_queryset().filter(menu__name=menu_object.name, user=user)

        if qs.exists():
            qs_object = super().get_queryset().get(menu__name=menu_object.name, user=user)
            menu_object_amount = qs_object.amount
        else:
            menu_object_amount = 0

        if amount_to_add + menu_object_amount > menu_object.stock:
            raise ValueError(f"Amount value can not be greater than {menu_object.name}'s stock value.")


class Cart(models.Model):
    menu = models.ForeignKey(Food, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    amount = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1, message='Amount can not be less than 1')])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = CartManager()

    def __str__(self):
        return self.menu.name

    class Meta:
        ordering = ['menu__name']


class Payment(models.Model):
    payment = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.payment
