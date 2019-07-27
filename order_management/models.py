from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=14, unique=True, null=True)
    email = models.EmailField('email address', unique=True)
    name = models.CharField(max_length=60)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Order(models.Model):
    product_url = models.URLField(max_length=300)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                             null=True, blank=True)
    note = models.TextField(max_length=1000,
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

    ORDER_STATUS = (
        (0, 'user query a request'),
        (1, 'user query result submitted'),
        (2, 'user place the order'),
        (3, 'product purchased'),
        (4, 'product in shipping'),
        (5, 'product arrived in eZon office'),
        (6, 'product delivered to the customer'),
        (7, 'order completed')
    )

    status = models.IntegerField(max_length=1, choices=ORDER_STATUS, default=0, help_text='order status')
    is_payment_complete = models.BooleanField(default=False)
    probable_product_handover_date = models.DateField(blank=True, null=True)
    # product_category should be added later

    class Meta:
        ordering = ['probable_product_handover_date', 'status']

    def __str__(self):
        return str(self.id) + " (" + self.product_url[:50] + ")"

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def get_total_price(self):
        if self.product_price==None or self.product_tax == None or self.product_service_fee == None:
            return "Product price is not updated"
        else:
            return self.product_price + self.product_service_fee + self.product_tax


class OrderProcessingDates(models.Model):
    oder = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)

    ORDER_STATUS = (
        (0, 'user query a request'),
        (1, 'user query result submitted'),
        (2, 'user place the order'),
        (3, 'product purchased'),
        (4, 'product in shipping'),
        (5, 'product arrived in eZon office'),
        (6, 'product delivered to the customer'),
        (7, 'order completed')
    )
    status = models.IntegerField(max_length=1, choices=ORDER_STATUS, default=0, help_text= 'Oder status')
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('orderProcessingDates-detail', args=[str(self.id)])


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    address = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = []

    def __str__(self):
        return str(self.user.name)

    def get_absolute_url(self):
        return reverse('userProfile-detail', args=[str(self.id)])
