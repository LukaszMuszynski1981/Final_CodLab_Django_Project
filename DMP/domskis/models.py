from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Rooms(models.Model):

    types = (
        ('1', 'Cela'),
        ('2', 'Komnata ze współbratem'),
        ('3', 'Klasyczna trójka z łazienką'),
        ('4', 'Dormitorium'),
    )

    type = models.CharField(choices=types, max_length=1)
    description = models.TextField()
    price = models.IntegerField()
    avalamount = models.IntegerField()
    available = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Instructors(models.Model):

    types = (
        ('1', 'Początkujący'),
        ('2', 'Średniozaawansowany'),
        ('3', 'Zaawansowany'),
    )

    type = models.CharField(choices=types, max_length=1)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.get_type_display())


class Reservations(models.Model):

    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arrival = models.DateField()
    departure = models.DateField()
    meal = models.NullBooleanField(default=False)
    instructor = models.NullBooleanField(default=False)
    additional_information = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room = models.ForeignKey(Rooms, on_delete=models.DO_NOTHING)
    instructors = models.ManyToManyField(Instructors, through='CourseDetails')

    def get_absolute_url(self):
        return '/my-reservation/{pk}'.format(pk=self.id)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.name, self.surname, self.arrival, self.departure,
                                       self.room.get_type_display())


class CourseDetails(models.Model):

    instructor = models.ForeignKey(Instructors, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
    course_user = models.CharField(max_length=200, null=True)
    adult = models.NullBooleanField(default=False)
    child = models.NullBooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.course_user, self.instructor, self.adult, self.child)

