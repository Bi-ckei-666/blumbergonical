# Generated by Django 3.2.12 on 2022-02-10 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0026_auto_20220208_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lighting',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='sub_category',
        ),
        migrations.DeleteModel(
            name='SubCat',
        ),
    ]
