# Generated by Django 2.0.5 on 2018-10-04 13:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0004_auto_20181004_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservations',
            name='reservation_id',
            field=models.SlugField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservations',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
