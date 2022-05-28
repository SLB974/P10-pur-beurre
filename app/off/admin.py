from django.contrib import admin

from .models import Category, Favorite, Product

# Register your models here.

admin.site.register([Category, Product, Favorite])
