# Generated by Django 2.2.3 on 2019-07-31 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0005_auto_20190731_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_price',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, help_text='Origin Amazon product price', max_digits=10, null=True),
        ),
    ]
