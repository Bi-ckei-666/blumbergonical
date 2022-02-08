# Generated by Django 3.2.7 on 2022-02-08 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0024_auto_20220204_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=255, verbose_name='Имя подкатегории')),
                ('cat_slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='lighting',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcat', verbose_name='Подкатегория'),
        ),
        migrations.AddField(
            model_name='nonstationarywire',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcat', verbose_name='Подкатегория'),
        ),
        migrations.AddField(
            model_name='notebook',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcat', verbose_name='Подкатегория'),
        ),
        migrations.AddField(
            model_name='smartphone',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.subcat', verbose_name='Подкатегория'),
        ),
    ]
