from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget

from .forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id', 'email', 'gender', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'gender')
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info',
         {'fields': (
             'first_name', 'last_name', 'gender', 'role', 'avatar',
             'location')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    add_fieldsets = (
        (None, {'fields': (
            'email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info',
         {'fields': (
             'first_name', 'last_name', 'gender', 'role', 'avatar',
             'location')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
