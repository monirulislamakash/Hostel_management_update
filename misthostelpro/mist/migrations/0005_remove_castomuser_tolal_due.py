# Generated by Django 3.2.6 on 2021-12-11 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mist', '0004_auto_20211211_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='castomuser',
            name='Tolal_Due',
        ),
    ]