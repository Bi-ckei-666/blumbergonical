# Generated by Django 3.2.12 on 2022-02-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_nonstationarywire'),
    ]

    operations = [
        migrations.AddField(
            model_name='lighting',
            name='count_view',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nonstationarywire',
            name='count_view',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='notebook',
            name='count_view',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='smartphone',
            name='count_view',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
