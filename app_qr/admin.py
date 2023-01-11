from django.contrib import admin
from .models import Category, Product, Resturant, Qr
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Resturant)
admin.site.register(Qr)




