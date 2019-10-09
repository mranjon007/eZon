from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.models import CustomUser
import datetime
from django.utils import timezone


ORDER_STATUS = (
    ('price_query', 'Price Query'),
    ('price_query_submitted', 'Price Query Submitted'),
    ('placed_order', 'Placed Order'),
    ('product_purchase_request', 'Product Purchase Request'),
    ('purchase_canceled', 'Purchase Canceled'),
    ('product_purchased', 'Product Purchased'),
    ('product_arrived_in_usa_office', 'Product Arrived in USA Office'),
    ('product_in_shipping', 'Product in Shipping'),
    ('product_arrived_in_ezon_office', 'Product Arrived In eZon Office'),
    ('product_send_to_delivery_person', 'Product Send to Delivery Person'),
    ('product_delivery_canceled', 'Product Delivery Canceled'),
    ('product_delivered_to_the_customer', 'Product Delivered To The Customer'),
    ('order_completed', 'Order Completed'),
    ('order_canceled', 'Order Canceled'),
    ('order_refunded', 'Order Refunded'),
    ('order_defected', 'Product Defected'),
)

COMPANY_LISTING = (
    ('amazon', 'Amazon'),
    ('ebay', 'Ebay'),
    ('walmart', 'Walmart'),
    ('others', 'Others'),
)

COUNTRY_LIST = (
    ('usa', 'USA'),
    ('uk', 'UK'),
    ('others', 'Others')
)

PAYMENT_STATUS = (
    ('not_paid', 'Not Paid'),
    ('partially_paid', 'Partially Paid'),
    ('full_paid', 'Full Paid'),
)

PAYMENT_WAY = (
    ('cash_on_delivery', 'Cash On Delivery'),
    ('bkash', 'bKash'),
    ('card', 'Card'),
    ('bank', 'Bank'),
)


class Order(models.Model):
    product_url = models.URLField(max_length=300)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                             null=True, blank=True)
    customer_note = models.TextField(max_length=1000,
                                     help_text="Please provide a detail description(size, color,..etc) "
                                               "for your product", null=True, blank=True)
    admin_note = models.TextField(max_length=1000,
                                  help_text="Please provide a detail description(size, color,..etc) "
                                            "for your product", null=True, blank=True)

    product_price = models.DecimalField(max_digits=10, decimal_places=3,
                                        help_text='Origin Amazon product price',
                                        default=0)
    product_tax = models.DecimalField(max_digits=10, decimal_places=3,
                                      help_text='Tax for the product', default=0)
    product_service_fee = models.DecimalField(max_digits=10, decimal_places=3,
                                              help_text='Service fee for the product',
                                              default=0)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='price_query', help_text='Order status')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='not_paid')
    probable_product_handover_date = models.DateField(blank=True, null=True)

    product_company = models.CharField(max_length=50, choices=COMPANY_LISTING, default='amazon',)

    product_country = models.CharField(max_length=50, choices=COUNTRY_LIST, default='usa')
    purchase_id = models.CharField(max_length=200, blank=True, null=True)
    # product_category should be added later

    class Meta:
        ordering = ['id']

    def get_order_number(self):
        return str(self.id + 1000)  # 1000 + id number

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def get_total_price(self):
        if self.product_price is None or self.product_tax is None or self.product_service_fee is None:
            return "Product price is not updated"
        else:
            return self.product_price + self.product_service_fee + self.product_tax


class OrderProcessingDate(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_status_dates')

    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='price_query', help_text='Order status')
    date = models.DateTimeField(null=False, default=timezone.now)
    note = models.TextField(max_length=400, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('orderProcessingDate-detail', args=[str(self.id)])


class DeliveryInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_info')
    delivery_person = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                             null=True, blank=True)
    note = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = []

    def __str__(self):
        return str(self.order.id + " | " + self.provider_name)

    def get_absolute_url(self):
        return reverse('DeliveryProvider-detail', args=[str(self.id)])


class PaymentDates(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='payment_dates')
    payment_way = models.CharField(max_length=40, choices=PAYMENT_WAY)
    Date = models.DateTimeField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('paymentDates-detail', args=[str(self.id)])

