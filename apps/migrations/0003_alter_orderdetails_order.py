# Generated by Django 4.1.7 on 2023-03-30 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_rename_order_id_orderdetails_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='apps.orders', verbose_name='ИД заказа'),
        ),
    ]