# Generated by Django 2.2.3 on 2019-07-31 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0006_auto_20190731_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderprocessingdate',
            name='notes',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
