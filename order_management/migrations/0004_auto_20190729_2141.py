# Generated by Django 2.2.3 on 2019-07-29 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0003_auto_20190729_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Request Price'), (1, 'Query Result Submitted'), (2, 'Place Order'), (3, 'product purchased'), (4, 'product in shipping'), (5, 'product arrived in eZon office'), (6, 'product delivered to the customer'), (7, 'order completed'), (8, 'order canceled'), (9, 'order refunded'), (10, 'product defected')], default=0, help_text='order status'),
        ),
    ]
