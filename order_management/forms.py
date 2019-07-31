from django import forms


COMPANY_LISTING = (
    (0, 'Amazon'),
    (1, 'Ebay'),
    (2, 'Walmart'),
    (3, 'Others')
)


class PriceQueryForm(forms.Form):
    product_url = forms.URLField(max_length=300, required=True, initial='https://')
    product_company = forms.ChoiceField(choices=COMPANY_LISTING, required=False)
