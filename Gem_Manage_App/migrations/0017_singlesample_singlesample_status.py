# Generated by Django 3.1.3 on 2020-11-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gem_Manage_App', '0016_auto_20201129_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlesample',
            name='SingleSample_status',
            field=models.CharField(default=1, max_length=20),
        ),
    ]
