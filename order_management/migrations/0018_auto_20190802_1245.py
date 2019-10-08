# Generated by Django 2.2.3 on 2019-08-02 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0017_auto_20190802_0506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='orderprocessingdate',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AlterField(
            model_name='deliveryinfo',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_info', to='order_management.Order'),
        ),
        migrations.AlterField(
            model_name='orderprocessingdate',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_status_dates', to='order_management.Order'),
        ),
        migrations.CreateModel(
            name='PaymentDates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('partially_paid', 'Partially Paid'), ('full_paid', 'Full Paid')], max_length=40)),
                ('payment_way', models.CharField(choices=[('cash_on_delivery', 'Cash On Delivery'), ('bkash', 'Bkash'), ('card', 'Card'), ('bank', 'Bank')], max_length=40)),
                ('Date', models.DateTimeField()),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_dates', to='order_management.Order')),
            ],
        ),
    ]