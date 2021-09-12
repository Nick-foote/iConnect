from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.translation import gettext as _

from users.models import Profile, User


# ------------------------------------------------------------------------------------------------
#   --   Admin Functions    --

def verify_users(modeladmin, request, queryset):
    queryset.update(is_verified=True)


# ------------------------------------------------------------------------------------------------
#   --   Models    --

verify_users.short_description = 'Verify Selected Users'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'first_name', 'last_name', 'username']
    search_fields = ['first_name', 'last_name', 'username']
    list_per_page = 50

    fieldsets = (
        (_("Personal Info"), {'fields': (
            'email', 
            'username', 
            'password',
            'first_name', 
            'last_name',
            'dob',
            )}),
        (_('Permissions'), {'fields': (
            'is_private',
            'is_active',
            'is_verified',
            'is_staff',
            'is_superuser',
        )}),
        (_('Important Dates'), {'fields': ('date_joined', 'last_login', )}),

            
     )
    readonly_fields = ('date_joined', 'last_login', 'dob',)
    actions = [verify_users]

    def dob(self, obj):
        return obj.profile.dob


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ['user']
    list_display = ['id', 'user']
    search_fields = ['user__username']
    autocomplete_fields = ['user']
    list_per_page = 50
    readonly_fields = ('user',)
