# Generated by Django 3.2.6 on 2021-12-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mist', '0005_remove_castomuser_tolal_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='castomuser',
            name='hostel_incharje',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='castomuser',
            name='Gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10),
        ),
    ]
