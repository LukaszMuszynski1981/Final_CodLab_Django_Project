# Generated by Django 2.0.5 on 2019-04-07 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domskis', '0019_auto_20190407_1819'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_user', models.CharField(max_length=200, null=True)),
                ('adult', models.IntegerField(null=True)),
                ('child', models.IntegerField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='domskis.Instructors')),
            ],
        ),
        migrations.RemoveField(
            model_name='reservationsinstructors',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='reservationsinstructors',
            name='reservation',
        ),
        migrations.RemoveField(
            model_name='reservations',
            name='instructors',
        ),
        migrations.DeleteModel(
            name='ReservationsInstructors',
        ),
        migrations.AddField(
            model_name='coursedetails',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domskis.Reservations'),
        ),
    ]
