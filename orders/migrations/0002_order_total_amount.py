# Generated by Django 4.0.6 on 2023-01-24 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(default=1),
        ),
    ]
