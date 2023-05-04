from django.db import models
from django.utils import timezone
from django.conf import settings


class Order(models.Model):
    date = models.DateField()
    products = models.JSONField()
    email_address = models.EmailField()
    payment_type = models.CharField(max_length=100)
    total_amount = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=100, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.pk}"

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        self.date = timezone.now()
        super().save(*args, **kwargs)
