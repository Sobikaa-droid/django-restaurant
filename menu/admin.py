from django.contrib import admin
from .models import Food, Category

admin.site.register([Food, Category])
