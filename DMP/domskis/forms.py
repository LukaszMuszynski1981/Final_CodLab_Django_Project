from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime, timedelta
from .models import Reservations, Rooms


User = get_user_model()


def get_types_r():

    types_r = {}
    avaliable_types = Rooms.objects.exclude(avalamount__lte=0)
    for _ in avaliable_types.iterator():
        types_r[_.type] = _.description
    return tuple(sorted(types_r.items()))


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label='Użytkownik')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid user or password")
        self.user = user
        return cleaned_data


class ReservationForm(forms.Form):

    types_r = (
        ('0', '--'),
        ('1', 'Cela'),
        ('2', 'Komnata ze współbratem'),
        ('3', 'Klasyczna trójka z łazienką'),
        ('4', 'Dormitorium'),
    )

    types_i = (
        ('0', '--'),
        ('1', 'Początkujący'),
        ('2', 'Średniozaawansowany'),
        ('3', 'Zaawansowany'),
    )

    name = forms.CharField(
        max_length=100,
        label='Imię'
    )
    surname = forms.CharField(
        max_length=100,
        label='Nazwisko'
    )
    arrive = forms.CharField(label='Przyjazd')
    departure = forms.CharField(label='Wyjazd')
    room = forms.ChoiceField(
        widget=forms.Select,
        choices=types_r,
        label='Wybierz pokój'
    )
    meal = forms.NullBooleanField(label='Wyżywienie na miejscu')
    instructor = forms.NullBooleanField(label='Czy potrzebujesz intruktora?')
    i_name_one = forms.CharField(
        max_length=100,
        label='Imię',
        required=False
    )
    child_one = forms.BooleanField(label='Dziecko', required=False)
    adult_one = forms.BooleanField(label='Dorosły', required=False)
    instructors_one = forms.ChoiceField(
        widget=forms.Select,
        choices=types_i,
        label='Poziom'
    )
    i_name_two = forms.CharField(
        max_length=100,
        label='Imię',
        required=False
    )
    child_two = forms.BooleanField(label='Dziecko', required=False)
    adult_two = forms.BooleanField(label='Dorosły', required=False)
    instructors_two = forms.ChoiceField(
        widget=forms.Select,
        choices=types_i,
        label='Poziom'
    )
    i_name_three = forms.CharField(
        max_length=100,
        label='Imię',
        required=False
    )
    child_three = forms.BooleanField(label='Dziecko', required=False)
    adult_three = forms.BooleanField(label='Dorosły', required=False)
    instructors_three = forms.ChoiceField(
        widget=forms.Select,
        choices=types_i,
        label='Poziom'
    )


class MyReservationForm(forms.Form):

    id = forms.CharField(label='')


class UploadFileForm(forms.Form):

    file = forms.FileField()


class OnlyEmailForm(forms.Form):

    email = forms.CharField(label='E-mail', widget=forms.EmailInput)


class ResetPasswordForm(forms.Form):

    new_password1 = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput, strip=False)
    new_password2 = forms.CharField(label="Potwierdzenie hasła", widget=forms.PasswordInput, strip=False)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Wpisane hasła nie są jednakowe. Spróbuj ponownie")
        return password2

