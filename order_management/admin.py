from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import gettext, gettext_lazy as _
# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    # CustomUser,
    Order,
    OrderProcessingDate,
    DeliveryInfo,
)


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     list_display = ('email', 'name', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('name', 'password', 'phone_number',)}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProcessingDate)
class OrderProcessingDatesAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')

@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    pass
