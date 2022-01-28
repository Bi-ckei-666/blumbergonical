# Generated by Django 3.2.7 on 2021-11-30 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20211126_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Общая Цена'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer', verbose_name='Покупатель'),
        ),
    ]
