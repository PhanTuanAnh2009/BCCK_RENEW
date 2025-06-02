from django.contrib import admin
from .models import Product,CustomUser



admin.site.register(Product)
# admin.site.register(Products)
admin.site.register(CustomUser)

# Register your models here.
