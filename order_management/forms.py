from django import forms


COMPANY_LISTING = (
    (0, 'Amazon'),
    (1, 'Ebay'),
    (2, 'Walmart'),
    (3, 'Others')
)

COUNTRY_LIST = (
    (0, 'USA'),
    (1, 'UK'),
    (2, 'Others')
)


class PriceQueryForm(forms.Form):
    product_url = forms.URLField(max_length=300, required=True, initial='https://')
    product_company = forms.ChoiceField(choices=COMPANY_LISTING, required=False)


class PriceQueryUpdateForm(forms.Form):
    product_price = forms.DecimalField(max_digits=10, decimal_places=3, help_text='Origin Amazon product price',)
    product_tax = forms.DecimalField(max_digits=10, decimal_places=3, help_text='Enter Product Tax')
    product_service_fee = forms.DecimalField(max_digits=10, decimal_places=3, help_text='Enter Service Fee')
    admin_note = forms.CharField(max_length=1000,   widget=forms.Textarea, required=False)