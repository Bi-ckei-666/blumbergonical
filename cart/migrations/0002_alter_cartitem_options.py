# Generated by Django 4.2.5 on 2023-10-11 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины пользователей'},
        ),
    ]