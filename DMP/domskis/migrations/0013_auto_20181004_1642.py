# Generated by Django 2.0.5 on 2018-10-04 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0012_auto_20181004_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='instructor',
            field=models.BooleanField(default=False),
        ),
    ]
