# Generated by Django 2.2.3 on 2019-08-04 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0023_auto_20190804_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderprocessingdate',
            name='notes',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]