# Generated by Django 3.2.6 on 2021-12-06 18:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mist', '0002_auto_20211204_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='castomuser',
            name='Leave',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='demo',
            name='Date_Time',
            field=models.CharField(default=datetime.date(2021, 12, 7), max_length=50),
        ),
        migrations.AlterField(
            model_name='notice',
            name='Date',
            field=models.DateField(default=datetime.date(2021, 12, 7)),
        ),
        migrations.AlterField(
            model_name='payment_history',
            name='Date',
            field=models.DateField(default=datetime.date(2021, 12, 7)),
        ),
    ]