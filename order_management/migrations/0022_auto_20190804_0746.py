# Generated by Django 2.2.3 on 2019-08-04 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0021_auto_20190804_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_company',
            field=models.CharField(choices=[('amazon', 'Amazon'), ('ebay', 'Ebay'), ('walmart', 'Walmart'), ('others', 'Others')], default='amazon', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_country',
            field=models.CharField(choices=[('usa', 'USA'), ('uk', 'UK'), ('others', 'Others')], default='usa', max_length=50),
        ),
    ]
