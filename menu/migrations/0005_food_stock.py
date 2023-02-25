# Generated by Django 4.0.6 on 2022-12-22 19:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_food_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='stock',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
