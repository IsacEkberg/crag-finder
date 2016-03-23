from django.http import JsonResponse
from django.shortcuts import redirect


def development_index(request):
    return redirect('static/index.html')


def development_api_mock(request):
    return JsonResponse({'Key': "value"})

