# Generated by Django 4.0.4 on 2022-07-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0039_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(null=True, verbose_name='текст новости'),
        ),
    ]
