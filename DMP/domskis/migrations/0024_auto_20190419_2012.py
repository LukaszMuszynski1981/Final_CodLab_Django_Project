# Generated by Django 2.0.5 on 2019-04-19 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0023_auto_20190412_0849'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='amount',
            new_name='price',
        ),
    ]