from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import (
    COMPANY_LISTING,
    COUNTRY_LIST,
    PAYMENT_STATUS,
    PAYMENT_WAY,
    CURRENCY_LIST,
)

from user.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class PriceQueryForm(forms.Form):
    product_url = forms.URLField(max_length=300, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Product Url'}))

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}) )
    customer_note = forms.CharField(max_length=500, required=False, help_text=
                                    "Please specify product size, color, etc. if any",
                                    widget=forms.Textarea(attrs={'placeholder': 'Customer Note'}))

    email_address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=14, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                help_text=_("Enter the same password as above, for verification."))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'product_url',
            'name',
            'customer_note',
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('email_address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign in')
        )



# class PriceQueryForm(forms.Form):
#     product_url = forms.URLField(max_length=300, required=True, initial='https://')
#     customer_note = forms.CharField(max_length=500, widget=forms.Textarea,
#                                     required=False, help_text= "please specify product "
#                                                                "size, color, etc. if any")
#
#     name = forms.CharField(max_length=100)
#     phone_number = forms.CharField(max_length=13)
#     email_address = forms.CharField(max_length=80)
#
#     password1 = forms.CharField(label=_("Password"),
#                                 widget=forms.PasswordInput)
#     password2 = forms.CharField(label=_("Password confirmation"),
#                                 widget=forms.PasswordInput,
#                                 help_text=_("Enter the same password as above, for verification."))
#
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2


class PriceQueryUpdateForm(forms.Form):
    product_price = forms.DecimalField(max_digits=10, decimal_places=3,
                                       help_text='Origin Amazon product price')
    foreign_tax = forms.DecimalField(label="USA/UK tax", max_digits=10, decimal_places=3,
                                     help_text='Enter USA or UK Tax')
    foreign_shipping = forms.DecimalField(label="USA/UK shipping", max_digits=10,
                                          decimal_places=3, help_text='Enter USA or UK Shipping')
    bd_shipping = forms.DecimalField(label="bd shipping", max_digits=10,
                                     decimal_places=3, help_text='Enter USA or UK Shipping')
    bd_custom = forms.DecimalField(label="bd custom", max_digits=10, decimal_places=3,
                                   help_text='Enter USA or UK Shipping')
    service_charge = forms.DecimalField(max_digits=10, decimal_places=3,
                                        help_text='Enter exchange rate')
    mobile_or_bank_charge = forms.DecimalField(max_digits=10, decimal_places=3,
                                               help_text='Enter mobile banking charge/ general bank charge')
    currency = forms.ChoiceField(choices=CURRENCY_LIST)
    exchange_rate = forms.DecimalField(max_digits=10, decimal_places=3,
                                       help_text='Enter exchange rate of dollar or pound')

    admin_note = forms.CharField(max_length=500, widget=forms.Textarea, required=False)


class PlaceOrderForm(forms.Form):
    product_url = forms.URLField(max_length=300)
    product_url = forms.URLField(max_length=300)
    product_company = forms.ChoiceField(choices=COMPANY_LISTING)
    product_country = forms.ChoiceField(choices=COUNTRY_LIST)
    product_price = forms.DecimalField(max_digits=10, decimal_places=3,
                                       help_text='Origin Amazon product price')
    foreign_tax = forms.DecimalField(label="USA/UK tax", max_digits=10, decimal_places=3,
                                     help_text='Enter USA or UK Tax')
    foreign_shipping = forms.DecimalField(label="USA/UK shipping", max_digits=10,
                                          decimal_places=3, help_text='Enter USA or UK Shipping')
    bd_shipping = forms.DecimalField(label="bd shipping", max_digits=10,
                                     decimal_places=3, help_text='Enter USA or UK Shipping')
    bd_custom = forms.DecimalField(label="bd custom", max_digits=10, decimal_places=3,
                                   help_text='Enter USA or UK Shipping')
    service_charge = forms.DecimalField(max_digits=10, decimal_places=3,
                                        help_text='Enter exchange rate')
    mobile_or_bank_charge = forms.DecimalField(max_digits=10, decimal_places=3,
                                               help_text='Enter mobile banking charge/ general bank charge')
    currency = forms.ChoiceField(choices=CURRENCY_LIST)
    exchange_rate = forms.DecimalField(max_digits=10, decimal_places=3,
                                       help_text='Enter exchange rate of dollar or pound')
    payment_status = forms.ChoiceField(choices=PAYMENT_STATUS)
    admin_note = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)
    customer_name = forms.CharField(max_length=100)
    customer_phone_number = forms.CharField(max_length=13)
    customer_email_address = forms.CharField(max_length=80)
    customer_address = forms.CharField(max_length=300)
    customer_note = forms.CharField(max_length=500, widget=forms.Textarea, required=False)

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


class ProductPurchaseForm(forms.Form):
    purchase_id = forms.CharField(max_length=100, required=True, help_text='Please enter the purchase id')


class ProductPurchaseCancelForm(forms.Form):
    note = forms.CharField(label='Cancel Note', max_length=400, required=True, help_text='if you cancel \
                                                    the purchase then must provide the reason '
                                                                     'for canceling')


# class ProductPurchaseFrom(forms.Form):
#     purchase_id = forms.CharField(label='Purchase Id', max_length=100, required=True, help_text=""
#                                                     "Please enter the product id")


class ProductSendToDeliveryForm(forms.Form):
    delivery_person = forms.ChoiceField()
    note = forms.CharField(label='Delivery Note', max_length=400, required=True, help_text='delivery note')
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['delivery_person'].choices = [(u.id, u.name) for u in CustomUser.objects.filter(is_staff='True')]

class ProductDeliveryCancelFrom(forms.Form):
    note = forms.CharField(label='Delivery Cancel Note', max_length=400, required=True, help_text='if you cancel \
                                                    the delivery then must provide the reason '
                                                                     'for canceling')

