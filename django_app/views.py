from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.views import (
    password_reset_confirm,
    password_reset,
)
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def development_index(request):
    return HttpResponse("<p><b>Error: Wrong port!</b> <br> In order to run this project locally:</p>"
                        "<ol>"
                        "<li>Run nginx</li>"
                        "<li>Run 'ember server'</li>"
                        "<li>Run djangos 'manage.py runserver'</li>"
                        "</ol>"
                        "<p>For more details, checout the nginx_local_dev folder.</p>"
                        "<p>(If you have already done this, try 127.0.0.1:1337 instead)")


def development_api_mock(request):
    return JsonResponse({'Key': "value"})


def reset(request):
    return password_reset(request, template_name='django_api/pw_res.html',
                          email_template_name='django_api/pw_res_email.html',
                          subject_template_name='django_api/pw_res_email_subject.txt',
                          from_email='noreply@cragfinder.se')


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='django_api/pw_res_confirm.html',
                                  uidb64=uidb64,
                                  token=token,
                                  post_reset_redirect=reverse('password_reset_complete'))


def reset_done(request):
    messages.success(request,
                     "Ett mail kommer inom kort skickas till mailadressen som angavs. "
                     "I den finns en länk för att skapa ett nytt lösenord. "
                     "Om det inte kommer något mail vänligen kontrollera att du angivit rätt epost och försök igen.")
    return redirect(reverse("admin:login"))


def reset_complete(request):
    return redirect(reverse("admin:login"))
