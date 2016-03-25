from django.http import JsonResponse, HttpResponse


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

