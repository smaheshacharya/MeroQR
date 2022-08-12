from django.contrib import admin
from .models import Category, Product
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# class CategoryModelAdmin(BaseUserAdmin):
 
#     list_display = ('cat_name', 'cat_image','user_id')
#     fieldsets = (
#         ('Category Info', {'fields':('cat_name','slug','cat_description','cat_image')}),
#         ('Woner', {'fields': ('user_id')}),
#     )
   
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('cat_name','slug','cat_description','cat_image','user_id'),
#         }),
#     )
#     search_fields = ('cat_name','slug')
#     ordering = ('cat_name','slug','id','user_id')
#     filter_horizontal = ()


# class ProductModelAdmin(BaseUserAdmin):
 

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('name', 'price','user_id', 'category_id')
#     fieldsets = (
#         ('Product Info', {'fields': ('name','price','pro_description','pro_image')}),
#         ('Relation Field', {'fields': ('user_id','category_id')}),
#         # ('Dates', {'fields': ('created_at','updated_at')}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('name','price','pro_description','pro_image','user_id','category_id'),
#         }),
#     )
#     search_fields = ('name','price')
#     ordering = ('name','id','user_id','category_id')
#     filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Category)
admin.site.register(Product)




