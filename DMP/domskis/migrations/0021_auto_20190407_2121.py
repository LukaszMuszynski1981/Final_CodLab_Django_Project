# Generated by Django 2.0.5 on 2019-04-07 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0020_auto_20190407_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedetails',
            name='adult',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coursedetails',
            name='child',
            field=models.NullBooleanField(default=False),
        ),
    ]
