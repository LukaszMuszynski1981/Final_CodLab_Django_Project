# Generated by Django 2.0.5 on 2018-10-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0007_auto_20181004_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='reservation',
            field=models.SlugField(max_length=6, unique=True),
        ),
    ]
