# Generated by Django 4.0.6 on 2023-01-10 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_alter_food_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='menu.category'),
        ),
    ]
