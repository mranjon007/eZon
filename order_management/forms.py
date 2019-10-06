from django import forms
from .models import (
    COMPANY_LISTING,
    COUNTRY_LIST,
    PAYMENT_STATUS,
    PAYMENT_WAY
)
from user.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class PriceQueryForm(forms.Form):
    product_url = forms.URLField(max_length=300, required=True, initial='https://')
    product_company = forms.ChoiceField(choices=COMPANY_LISTING, required=False)


class PriceQueryUpdateForm(forms.Form):
    product_price = forms.DecimalField(max_digits=10, decimal_places=3, help_text='Origin Amazon product price',)
    product_tax = forms.DecimalField(max_digits=10, decimal_places=3, help_text='Enter Product Tax')
    product_service_fee = forms.DecimalField(max_digits=10, decimal_places=3, help_text='Enter Service Fee')
    admin_note = forms.CharField(max_length=1000,   widget=forms.Textarea, required=False)


class PlaceOrderForm(forms.Form):
    product_url = forms.URLField(max_length=300)
    product_company = forms.ChoiceField(choices=COMPANY_LISTING)
    product_country = forms.ChoiceField(choices=COUNTRY_LIST)
    product_price = forms.DecimalField(max_digits=10, decimal_places=3, help_text="Origin Product Price in BDT")
    product_tax = forms.DecimalField(max_digits=10, decimal_places=3, help_text="Product Tax in BDT")
    product_service_fee = forms.DecimalField(max_digits=10, decimal_places=3, help_text="Product Service Fee")
    payment_status = forms.ChoiceField(choices=PAYMENT_STATUS)
    admin_note = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)
    customer_name = forms.CharField(max_length=100)
    customer_phone_number = forms.CharField(max_length=13)
    customer_email_address = forms.CharField(max_length=80)
    customer_address = forms.CharField(max_length=300)
    customer_note = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)

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


class ProductPurchaseCancelFrom(forms.Form):
    note = forms.CharField(label='Cancel Note', max_length=400, required=True, help_text='if you cancel \
                                                    the purchase then must provide the reason '
                                                                     'for canceling')


# class ProductPurchaseFrom(forms.Form):
#     purchase_id = forms.CharField(label='Purchase Id', max_length=100, required=True, help_text=""
#                                                     "Please enter the product id")


class ProductSendToDeliveryForm(forms.Form):
    delivery_person = forms.ChoiceField()
    note = forms.CharField(label='Delivery Note', max_length=400, required=True, help_text='if you cancel \
                                                        the purchase then must provide the reason '
                                                                                         'for canceling')
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['delivery_person'].choices = [(u.id, u.name) for u in CustomUser.objects.filter(is_staff='True')]