from django.contrib import admin
from .models import Cart, Payment

admin.site.register([Cart, Payment])
