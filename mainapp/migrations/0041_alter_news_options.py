# Generated by Django 4.0.4 on 2022-07-15 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0040_alter_news_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]