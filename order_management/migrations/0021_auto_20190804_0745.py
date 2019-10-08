# Generated by Django 2.2.3 on 2019-08-04 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0020_auto_20190803_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_price',
            field=models.DecimalField(decimal_places=3, default=0, help_text='Origin Amazon product price', max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderprocessingdate',
            name='status',
            field=models.CharField(choices=[('price_query', 'Price Query'), ('query_result_submitted', 'Query Result Submitted'), ('placed_order', 'Placed Order'), ('product_purchase_request', 'Product Purchase Request'), ('product_purchased', 'product purchased'), ('product_in_shipping', 'product in shipping'), ('product_arrived_in_ezon_office', 'product arrived in eZon office'), ('product_delivered_to_the_customer', 'product delivered to the customer'), ('order_completed', 'order completed'), ('order_canceled', 'order canceled'), ('order_refunded', 'order refunded'), ('order_defected', 'product defected')], default='price_query', help_text='Order status', max_length=50),
        ),
    ]