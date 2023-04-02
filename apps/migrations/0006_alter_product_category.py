# Generated by Django 4.1.7 on 2023-03-30 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_alter_orderdetails_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='apps.category', verbose_name='Категория'),
        ),
    ]