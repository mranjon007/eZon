from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True, null=True)
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=60)
    username = models.CharField(max_length=40, unique=False, default='')
    address = models.CharField(max_length=300, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class CustomUserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL,
                             null=True, blank=True)
    address_line_1 = models.CharField('Address Line 1', max_length=200, null=True, blank=True,
                                               help_text='Enter Your Appartment Number/House Number')
    address_line_2 = models.CharField('Address Line 2', max_length=300, null=True, blank=True,
                                               help_text="Enter Your Street Address")
    city = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=50, null=True, blank=True)


class PhoneNumberVerification(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True)
    verification_code = models.PositiveIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], null=True)
    count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
    is_verified = models.BooleanField(default=False)
