# Generated by Django 4.1.7 on 2023-03-30 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_alter_orderdetails_order_alter_orders_delivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='apps.product', verbose_name='Продукт'),
        ),
    ]
