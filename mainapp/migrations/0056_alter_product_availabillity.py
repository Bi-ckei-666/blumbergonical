# Generated by Django 4.2.5 on 2023-09-08 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0055_product_availabillity_alter_product_characteristiks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='availabillity',
            field=models.BooleanField(null=True, verbose_name='наличие'),
        ),
    ]