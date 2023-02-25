from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Food(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='static/menu/images/')
    price = models.DecimalField(max_digits=100, decimal_places=2)
    stock = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    class Meta:
        ordering = ['name']

    def update_cart_object_values(self):
        from cart.models import Cart

        qs = Cart.objects.filter(menu__name=self.name)
        if self.stock == 0:
            qs.delete()
        else:
            for cart_object in qs:
                if self.stock < cart_object.amount:
                    cart_object.amount = cart_object.amount - (cart_object.amount - self.stock)
                cart_object.price = self.price * cart_object.amount
                cart_object.save()

    def save(self, *args, **kwargs):
        self.update_cart_object_values()
        super().save(*args, **kwargs)
