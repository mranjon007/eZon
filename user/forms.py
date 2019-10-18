from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, CustomUserProfile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('name', 'email', 'phone_number')
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class PhoneNumberVerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=4, help_text="Enter the verification code sent to your mobile number")


class CustomUserProfileForm(forms.Form):
    name = forms.CharField(max_length=200, help_text='User Name')
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly': 'True'}))
    phone_number = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'readonly': 'True'}))
    address_line_1 = forms.CharField(max_length=200, required=False,
                                      help_text='Enter Your Apartment Number/House Number')
    address_line_2 = forms.CharField(max_length=300, required=False,
                                      help_text="Enter Your Street Address")
    city = forms.CharField(max_length=50, help_text="Enter Your City", required=False)
    district = forms.CharField(max_length=50, required=False)
    postcode = forms.CharField(max_length=50, required=False)