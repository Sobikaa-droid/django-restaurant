# Generated by Django 4.0.6 on 2023-02-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='amount',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
