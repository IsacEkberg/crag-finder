import random
import string

from django.contrib.admin import filters
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets, filters

from .forms import NewUserForm
from .models import Area, Parking, Route, RockFace, Club, AreaImage, RockFaceImage
from .serializers import (
    AreaSerializer,
    RockFaceSerializer,
    ParkingSerializer,
    RouteSerializer,
    ClubSerializer,
    AreaImageSerializer, RockFaceImageSerializer)


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RockFaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RockFaceSerializer
    queryset = RockFace.objects.all()


class ParkingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()


class ClubViewSet(viewsets.ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()


class AreaImageViewSet(viewsets.ModelViewSet):
    serializer_class = AreaImageSerializer
    queryset = AreaImage.objects.all()


class RockFaceImageViewSet(viewsets.ModelViewSet):
    serializer_class = RockFaceImageSerializer
    queryset = RockFaceImage.objects.all()


def new_user_view(request):
    def random_string_generator(size=32, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.instance
            user.is_staff = True
            user.set_password(random_string_generator())  # pw must be set in order to restore it.
            user.save()
            messages.success(request, message="Ditt konto har skapats! Återställ lösenordet för att kunna logga in.")
            return redirect('admin_password_reset')
    else:
        form = NewUserForm()
    return render(request, template_name='django_api/new_user.html', context={
        'form': form,
    })