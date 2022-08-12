from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
 

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name','business_name', 'business_logo', 'is_admin','is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','business_name','unique_business_slug','business_logo')}),
        ('Permissions', {'fields': ('is_admin','is_active')}),
        # ('Dates', {'fields': ('created_at','updated_at')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','business_name','unique_business_slug','business_logo','password1', 'password2'),
        }),
    )
    search_fields = ('email','business_name')
    ordering = ('email','business_name','id')
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)



