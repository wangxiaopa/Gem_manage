# Generated by Django 3.1.3 on 2020-12-14 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gem_Manage_App', '0024_auto_20201209_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preinstall',
            name='sample_type',
            field=models.CharField(max_length=50, verbose_name='配置项目'),
        ),
        migrations.AlterField(
            model_name='preinstall',
            name='type',
            field=models.CharField(max_length=50, verbose_name='配置类型'),
        ),
    ]
