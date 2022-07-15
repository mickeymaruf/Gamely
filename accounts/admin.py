from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

# Register your models here.

class AccountAdmin(UserAdmin):
    def thumbnail(self):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(self.profile_pictureUrl))
    list_display = (thumbnail,'email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined')
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    list_filter = ('is_admin',)
    filter_horizontal = ()
    fieldsets = ()
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
    )

admin.site.register(Account, AccountAdmin)

# unregister the Group model from admin.
admin.site.unregister(Group)