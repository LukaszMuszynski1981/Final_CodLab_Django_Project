import datetime as dt
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.views import View
from django.contrib.auth import get_user_model, login, logout
from django.template.response import TemplateResponse
from .models import Reservations, Rooms, Instructors, CourseDetails
from .forms import (
    SignupForm,
    LoginForm,
    ReservationForm,
    ResetPasswordForm,
    UploadFileForm,
    OnlyEmailForm,
)


User = get_user_model()


def get_user(request):

    session_key = str(request.session.session_key)
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    return user


def get_a_room(request):

    room_type = request.POST.get('room')
    rented_room = Rooms.objects.get(type=room_type)
    return rented_room


def get_instructor(request, particular_instructor):

    instructor_type = request.POST.get(particular_instructor)
    chosen_instructor = Instructors.objects.get(type=instructor_type)
    return chosen_instructor


def send_email(request, raw_message, raw_message_details=None):

    current_site = get_current_site(request)
    email = get_user(request).email
    mail_subject = 'Potwierdzenie rezerwacji'
    message = render_to_string('usertemplates/general_email_form.html', {
        'message': raw_message,
        'details': raw_message_details,
        'domain': current_site
    })
    email_msg = EmailMessage(
        mail_subject, message, to=[email]
    )
    email_msg.send()


def sign_up(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                u = User.objects.get(email=email)
                if u and not u.is_active:
                    u.delete()
                else:
                    return TemplateResponse(request, 'usertemplates/login_form.html', {
                        'form': LoginForm(),
                        'msg': 'Wszystko wskazuje na to, że już się zarejestrowałeś'
                    })
            except User.DoesNotExist:
                u = None
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta DMP Korbielów 2019.'
            message = render_to_string('usertemplates/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            # to_email = form.cleaned_data.get('email')
            email_msg = EmailMessage(
                mail_subject, message, to=[email]
            )
            email_msg.send()
            return TemplateResponse(request, 'usertemplates/login_form.html', {
                'form': LoginForm(),
                'msg': 'Na Twojego maila wysłalismy link. Klikając w niego potwierdzisz,\
             że Ty to Ty'
            })

    else:
        form = SignupForm()
    return render(request, 'usertemplates/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('main_auth')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def confirm_reset(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'GET':
        if user is not None and account_activation_token.check_token(user, token):
            return TemplateResponse(request, 'usertemplates/reset_password_form.html', {
                'form': ResetPasswordForm()
            })

    if request.method == 'POST':
        new_password = request.POST['new_password2']
        if user is not None:
            user.set_password(new_password)
            user.save()
            login(request, user)
            return redirect(to='main_auth')


def validate_dates_serializer(arr_date, dep_date):

    valid_rooms = {}

    reservations = Reservations.objects.all()
    for reservation in reservations.iterator():
        if reservation.arrival <= arr_date < reservation.departure or \
                                reservation.arrival < dep_date <= reservation.departure:
            try:
                valid_rooms[reservation.room.type] += 1
            except KeyError:
                valid_rooms[reservation.room.type] = 1

    rooms = Rooms.objects.all()
    for room in rooms.iterator():
        for k, v in valid_rooms.items():
            if room.type == k and v >= room.avalamount:
                valid_rooms[room.type] = 'not available'

    return valid_rooms


class LoginView(View):

    def get(self, request):

        return TemplateResponse(request, 'usertemplates/login_form.html', {
            'form': LoginForm()
        })

    def post(self, request):

        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(to='main_auth')
        else:
            ctx = {'form': LoginForm(),
                   'msg': 'Login lub hasło są nieprawidłowe. Spróbuj ponownie'
                   }
            return TemplateResponse(request, 'usertemplates/login_form.html', ctx)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(to='main')


class MainView(View):

    def get(self, request):
        return TemplateResponse(request, 'usertemplates/base.html', {'main': 'Miło Cię widzieć'})


class MainAuthView(View):

    def get(self, request):
        if request.session.session_key is None:
            return redirect(to='logout')

        try:
            user = get_user(request)
        except User.DoesNotExist:
            return redirect(to='logout')

        return TemplateResponse(request, 'usertemplates/base_auth.html', {
            'main': 'Miło Cię widzieć ' + user.username,
        })


class ReservationView(View):

    def get(self, request):

        if request.is_ajax():
            requested_type = request.GET['requested_type']
            arr_date = dt.datetime.strptime(request.GET['arriveDate'], '%Y-%m-%d')
            dep_date = dt.datetime.strptime(request.GET['departureDate'], '%Y-%m-%d')
            room = Rooms.objects.get(type=requested_type)
            days_spend = dep_date - arr_date
            return JsonResponse({
                'price': room.price * days_spend.days,
                'meal': 60 * days_spend.days,
                'instructor': 50
            })

        else:
            return TemplateResponse(request, 'usertemplates/reservationview_form.html', {
                'form': ReservationForm(),
                'msg_ins': '*(Te pola nie są wymagane)'
            })

    def post(self, request):

        if request.is_ajax():
            arr_date = dt.datetime.strptime(request.POST['arriveDate'], '%Y-%m-%d').date()
            dep_date = dt.datetime.strptime(request.POST['departureDate'], '%Y-%m-%d').date()
            validated_dates = validate_dates_serializer(arr_date, dep_date)
            return JsonResponse({'notAvailableRooms': validated_dates})

        user = get_user(request)
        form = ReservationForm(data=request.POST, files=request.FILES)
        rented_room = get_a_room(request)

        if form.is_valid():
            r = Reservations.objects.create(
                name=form.cleaned_data['name'],
                surname=form.cleaned_data['surname'],
                arrival=form.cleaned_data['arrive'],
                departure=form.cleaned_data['departure'],
                meal=form.cleaned_data['meal'],
                instructor=form.cleaned_data['instructor'],
                user_id=user.id,
                room=rented_room
            )
            if form.cleaned_data['adult'] or form.cleaned_data['child']:
                CourseDetails.objects.create(
                    instructor=get_instructor(request, 'instructors'),
                    reservation=r,
                    course_user=form.cleaned_data['i_name'],
                    adult=form.cleaned_data['adult'],
                    child=form.cleaned_data['child']
                )

            if form.cleaned_data['adult_two'] or form.cleaned_data['child_two']:
                CourseDetails.objects.create(
                    instructor=get_instructor(request, 'instructors_two'),
                    reservation=r,
                    course_user=form.cleaned_data['i_name_two'],
                    adult=form.cleaned_data['adult_two'],
                    child=form.cleaned_data['child_two']
                )

            if form.cleaned_data['adult_three'] or form.cleaned_data['child_three']:
                CourseDetails.objects.create(
                    instructor=get_instructor(request, 'instructors_three'),
                    reservation=r,
                    course_user=form.cleaned_data['i_name_three'],
                    adult=form.cleaned_data['adult_three'],
                    child=form.cleaned_data['child_three']
                )

            r_details = r.coursedetails_set.filter(
                    course_user__iregex=r'[1-9a-xA-Z]+'
                ).order_by('updated_at')
            send_email(request, r, r_details)

            return TemplateResponse(request, 'usertemplates/base_auth.html', {
                'main': 'Numer Twojej rezerwacji - {}'.format(r.id)
            })

        else:

            return TemplateResponse(request, 'usertemplates/reservationview_form.html', {
                'form': ReservationForm(),
                'msg': 'Nie wszystko poszło zgodnie z planem. Spróbuj jeszcze raz, upewnij się, że wszystkie pola '\
                       'są wypełenione'

            })


class MyReservationView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect(to='login')

        user_id = get_user(request).id
        try:
            reservation = Reservations.objects.filter(user_id=user_id).order_by('created_at')
            answer = TemplateResponse(request, 'usertemplates/myreservationview__form.html', {
                    'reservations': reservation,
                    'msg': reservation[0].user
                })
            return answer
        except IndexError:
            answer = TemplateResponse(request, 'usertemplates/base_auth.html', {
                'main': 'Nie masz żadnych rezerwacji'
            })

        return answer


class ProperReservationView(View):

    def get(self, request, reservation_id):

        if not request.user.is_authenticated:
            return redirect(to='login')

        reservation = Reservations.objects.get(id=reservation_id)
        course_details = reservation.coursedetails_set.filter(
            course_user__iregex=r'[1-9a-xA-Z]+'
        ).order_by('updated_at')
        answer = TemplateResponse(request, 'usertemplates/properreservationview__form.html', {
            'msg': 'Szczegóły rezerwacji',
            'reservation': reservation,
            'courseDetails': course_details,
            'form': UploadFileForm()
        })

        return answer

    def post(self, request, reservation_id):

        if request.is_ajax():
            Reservations.objects.filter(pk=reservation_id).delete()
            return JsonResponse({"redirect": 'true', "redirect_url": "http://127.0.0.1:8000/my-reservation"})
        else:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                reservation = Reservations.objects.get(id=reservation_id)
                reservation.file = request.FILES['file']
                reservation.save()
                if get_user(request):
                    return TemplateResponse(request, 'usertemplates/base_auth.html', {
                        'main': 'Plik został poprawnie załadowany. Dzięki i do zobaczenia'
                    })
                else:
                    return redirect('main_auth')
            else:
                return redirect(to='my-reservation')


class ResetPasswordView(View):

    def get(self, request):
        return TemplateResponse(request, 'usertemplates/only_email_form.html', {
            'form': OnlyEmailForm(),
            'msg': 'Zmiana hasła'
        })

    def post(self, request):

        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return TemplateResponse(request, 'usertemplates/login_form.html', {
                'form': OnlyEmailForm(),
                'msg': 'Adres mailowy jest niepoprawny'
            })
        current_site = get_current_site(request)
        mail_subject = 'Zmiana hasła w serwisie DMP'
        message = render_to_string('usertemplates/reset_password_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        email_msg = EmailMessage(
            mail_subject, message, to=[email]
        )
        email_msg.send()
        return TemplateResponse(request, 'usertemplates/base.html', {
            'msg': 'Na Twojego maila wysłalismy link potwierdzjący zmianę hasła'
        })
