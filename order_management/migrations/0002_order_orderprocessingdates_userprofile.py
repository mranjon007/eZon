# Generated by Django 2.2.3 on 2019-07-26 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_url', models.URLField(max_length=300)),
                ('note', models.TextField(blank=True, help_text='Please provide a detail description(size, color,..etc) for your product', max_length=1000, null=True)),
                ('product_price', models.DecimalField(blank=True, decimal_places=3, help_text='Origin Amazon product price', max_digits=10, null=True)),
                ('product_tax', models.DecimalField(blank=True, decimal_places=3, help_text='Tax for the product', max_digits=10, null=True)),
                ('product_service_fee', models.DecimalField(blank=True, decimal_places=3, help_text='Service fee for the product', max_digits=10, null=True)),
                ('status', models.IntegerField(choices=[(0, 'user query a request'), (1, 'user query result submitted'), (2, 'user place the order'), (3, 'product purchased'), (4, 'product in shipping'), (5, 'product arrived in eZon office'), (6, 'product delivered to the customer'), (7, 'order completed')], default=0, help_text='order status', max_length=1)),
                ('is_payment_complete', models.BooleanField(default=False)),
                ('probable_product_handover_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['probable_product_handover_date', 'status'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProcessingDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'user query a request'), (1, 'user query result submitted'), (2, 'user place the order'), (3, 'product purchased'), (4, 'product in shipping'), (5, 'product arrived in eZon office'), (6, 'product delivered to the customer'), (7, 'order completed')], default=0, help_text='Oder status', max_length=1)),
                ('date', models.DateField(auto_now=True)),
                ('oder', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='order_management.Order')),
            ],
            options={
                'ordering': ['status'],
            },
        ),
    ]