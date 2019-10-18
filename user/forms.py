from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


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


class CustomAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):

        if not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')


class PhoneNumberVerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=4, help_text="Enter the verification code sent to your mobile number")
    # def clean_customer_email_address(self):
    #     email = self.cleaned_data['customer_email_address']
    #     if CustomUser.objects.get(email=email):
    #         raise ValidationError(_("this email is already exist"))
    #     # Remember to always return the cleaned data.
    #     return email
    #
    # def clean_customer_phone_number(self):
    #     phone_number = self.cleaned_data['customer_phone_number']
    #     if CustomUser.objects.filter(phone_number=phone_number):
    #         raise ValidationError(_('this phone number is already exist'))
