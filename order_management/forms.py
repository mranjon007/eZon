from django import forms
from .models import (
    COMPANY_LISTING,
    COUNTRY_LIST,
    PAYMENT_STATUS,
    PAYMENT_WAY
)


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
