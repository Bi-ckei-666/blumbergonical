# Generated by Django 3.2.7 on 2021-11-16 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20211110_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphone',
            name='sd_volume',
            field=models.CharField(max_length=255, verbose_name='Максимальный объем SD карты'),
        ),
    ]
