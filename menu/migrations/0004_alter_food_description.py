# Generated by Django 4.0.6 on 2022-12-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_food_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
