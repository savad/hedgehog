from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from applications.accounts.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'followers_count', 'following_count', )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'followers_count',
                                         'following_count', 'home_town',
                                         'phone_number', 'profile_description')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('first_name', 'last_name', 'username')
    ordering = ('username', )


admin.site.register(User, CustomUserAdmin)
