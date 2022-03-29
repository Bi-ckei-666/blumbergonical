
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0036_auto_20220325_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lampa',
            name='power',
            field=models.CharField(blank=True, max_length=255, verbose_name='Мощность'),
        ),
    ]
