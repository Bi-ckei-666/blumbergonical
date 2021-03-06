# Generated by Django 3.2.7 on 2022-02-16 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0028_auto_20220210_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lighting',
            name='category',
        ),
        migrations.RemoveField(
            model_name='lighting',
            name='description',
        ),
        migrations.RemoveField(
            model_name='lighting',
            name='id',
        ),
        migrations.RemoveField(
            model_name='lighting',
            name='image',
        ),
        migrations.RemoveField(
            model_name='lighting',
            name='price',
        ),
        migrations.RemoveField(
            model_name='lighting',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='lighting',
            name='title',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='category',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='description',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='id',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='image',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='price',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='nonstationarywire',
            name='title',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='category',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='description',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='id',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='image',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='price',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='notebook',
            name='title',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='category',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='description',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='id',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='image',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='price',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='smartphone',
            name='title',
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='????????????????????????')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='??????????????????????')),
                ('description', models.TextField(null=True, verbose_name='????????????????')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='????????')),
                ('count_views', models.PositiveIntegerField(default=0, verbose_name='????????????????????')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='??????????????????')),
            ],
        ),
        migrations.AddField(
            model_name='lighting',
            name='product_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nonstationarywire',
            name='product_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notebook',
            name='product_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smartphone',
            name='product_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.product'),
            preserve_default=False,
        ),
    ]
