# Generated by Django 3.2.12 on 2022-03-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0034_auto_20220315_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='имя категории')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
