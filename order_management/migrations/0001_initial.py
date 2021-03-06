# Generated by Django 2.2.3 on 2019-07-28 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_url', models.URLField(max_length=300)),
                ('note', models.TextField(blank=True, help_text='Please provide a detail description(size, color,..etc) for your product', max_length=1000, null=True)),
                ('product_price', models.DecimalField(decimal_places=3, default=0, help_text='Origin Amazon product price', max_digits=10)),
                ('product_tax', models.DecimalField(decimal_places=3, default=0, help_text='Tax for the product', max_digits=10)),
                ('product_service_fee', models.DecimalField(decimal_places=3, default=0, help_text='Service fee for the product', max_digits=10)),
                ('status', models.IntegerField(choices=[(0, 'Request Price'), (1, 'Query Result Submitted'), (2, 'Place Order'), (3, 'product purchased'), (4, 'product in shipping'), (5, 'product arrived in eZon office'), (6, 'product delivered to the customer'), (7, 'order completed')], default=0, help_text='order status', max_length=1)),
                ('is_payment_complete', models.BooleanField(default=False)),
                ('probable_product_handover_date', models.DateField(blank=True, null=True)),
                ('product_company', models.IntegerField(blank=True, choices=[(0, 'Amazon'), (1, 'Ebay'), (2, 'Walmart')], null=True)),
                ('product_country', models.IntegerField(blank=True, choices=[(0, 'USA'), (1, 'UK')], null=True)),
            ],
            options={
                'ordering': ['probable_product_handover_date', 'status'],
            },
        ),
        migrations.CreateModel(
            name='OrderProcessingDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'user query a request'), (1, 'user query result submitted'), (2, 'user place the order'), (3, 'product purchased'), (4, 'product in shipping'), (5, 'product arrived in eZon office'), (6, 'product delivered to the customer'), (7, 'order completed')], default=0, help_text='Oder status', max_length=1)),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'ordering': [],
            },
        ),
    ]
