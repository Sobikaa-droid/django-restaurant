# Generated by Django 4.0.6 on 2023-01-10 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_category_food_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='categories',
            field=models.ManyToManyField(blank=True, to='menu.category'),
        ),
    ]
