# Generated by Django 2.2.3 on 2019-08-03 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0019_auto_20190803_0350'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentdates',
            options={'ordering': ['order']},
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
