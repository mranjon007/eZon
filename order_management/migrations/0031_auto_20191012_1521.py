# Generated by Django 2.2.6 on 2019-10-12 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0030_auto_20191004_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('price_query', 'Price Query'), ('price_query_submitted', 'Price Query Submitted'), ('placed_order', 'Placed Order'), ('product_purchase_request', 'Product Purchase Request'), ('purchase_canceled', 'Purchase Canceled'), ('product_purchased', 'Product Purchased'), ('product_arrived_in_usa_office', 'Product Arrived in USA Office'), ('product_in_shipping', 'Product in Shipping'), ('product_arrived_in_ezon_office', 'Product Arrived In eZon Office'), ('product_send_to_delivery_person', 'Product Send to Delivery Person'), ('product_delivery_canceled', 'Product Delivery Canceled'), ('product_delivered_to_the_customer', 'Product Delivered To The Customer'), ('order_completed', 'Order Completed'), ('order_canceled', 'Order Canceled'), ('order_refunded', 'Order Refunded'), ('order_defected', 'Product Defected')], default='price_query', help_text='Order status', max_length=50),
        ),
        migrations.AlterField(
            model_name='orderprocessingdate',
            name='status',
            field=models.CharField(choices=[('price_query', 'Price Query'), ('price_query_submitted', 'Price Query Submitted'), ('placed_order', 'Placed Order'), ('product_purchase_request', 'Product Purchase Request'), ('purchase_canceled', 'Purchase Canceled'), ('product_purchased', 'Product Purchased'), ('product_arrived_in_usa_office', 'Product Arrived in USA Office'), ('product_in_shipping', 'Product in Shipping'), ('product_arrived_in_ezon_office', 'Product Arrived In eZon Office'), ('product_send_to_delivery_person', 'Product Send to Delivery Person'), ('product_delivery_canceled', 'Product Delivery Canceled'), ('product_delivered_to_the_customer', 'Product Delivered To The Customer'), ('order_completed', 'Order Completed'), ('order_canceled', 'Order Canceled'), ('order_refunded', 'Order Refunded'), ('order_defected', 'Product Defected')], default='price_query', help_text='Order status', max_length=50),
        ),
    ]
