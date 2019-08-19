"""DMP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from domskis.views import (
    sign_up,
    activate,
    LoginView,
    LogoutView,
    MainView,
    MainAuthView,
    ReservationView,
    MyReservationView,
    ResetPasswordView,
    confirm_reset,
    ProperReservationView,
    AfterSuccessfulReservationView,
    AfterSuccessfulUploadView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('signup', sign_up, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
            activate, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('main-auth/', MainAuthView.as_view(), name='main-auth'),
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('my-reservation/', MyReservationView.as_view(), name='my-reservation'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('my-reservation/upload-success', AfterSuccessfulUploadView.as_view(), name='upload-success'),
    path('reservation/success', AfterSuccessfulReservationView.as_view(), name='success'),
    re_path(r'^my-reservation/(?P<reservation_id>[0-9]+$)', ProperReservationView.as_view(), name='reservation-id'),
    re_path(r'^reset-password/confirm-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
            confirm_reset, name='confirm-reset'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

