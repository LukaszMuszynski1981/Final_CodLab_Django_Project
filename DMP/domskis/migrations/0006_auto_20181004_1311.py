# Generated by Django 2.0.5 on 2018-10-04 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0005_auto_20181004_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='reservation_id',
            field=models.SlugField(auto_created=True, max_length=6),
        ),
    ]
