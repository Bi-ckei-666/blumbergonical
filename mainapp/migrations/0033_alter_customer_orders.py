# Generated by Django 3.2.7 on 2022-03-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0032_auto_20220315_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='related_customer', to='mainapp.Order', verbose_name='Заказы полкупателя'),
        ),
    ]