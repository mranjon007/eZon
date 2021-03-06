from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    CustomUser,
    PhoneNumberVerification,
    CustomUserProfile,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('name', 'password', 'phone_number',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(PhoneNumberVerification)
class PhoneNumberVerificationAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUserProfile)
class CustomUserProfileAdmin(admin.ModelAdmin):
    pass

