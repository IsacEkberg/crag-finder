import json

import random
import string

from django.contrib.admin import filters
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from rest_framework import viewsets, filters

from .models import Area, Parking, Route, RockFace, Club, AreaImage, RockFaceImage, APPROVED, BEING_REVIEWED_DELETE, \
    Access, RouteNode
from .forms import NewUserForm
from .models import Area, Parking, Route, RockFace, Club, AreaImage, RockFaceImage
from .serializers import (
    AreaSerializer,
    RockFaceSerializer,
    ParkingSerializer,
    RouteSerializer,
    ClubSerializer,
    AreaImageSerializer,
    RockFaceImageSerializer,
    AccessSerializer,
    RouteNodeSerializer)


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RockFaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RockFaceSerializer
    queryset = RockFace.objects.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class ParkingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class ClubViewSet(viewsets.ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class AreaImageViewSet(viewsets.ModelViewSet):
    serializer_class = AreaImageSerializer
    queryset = AreaImage.objects.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class RockFaceImageViewSet(viewsets.ModelViewSet):
    serializer_class = RockFaceImageSerializer
    queryset = RockFaceImage.objects.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class AccessViewSet(viewsets.ModelViewSet):
    serializer_class = AccessSerializer
    queryset = Access.objects.filter(Q(stop_date__gte=timezone.now()) | Q(stop_date__isnull=True))


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


class RouteNodeViewSet(viewsets.ModelViewSet):
    serializer_class = RouteNodeSerializer
    queryset = RouteNode.objects.all()


#TODO: Finish view.
def save_route_nodes(request, pk):
    if request.method == 'POST':
        data = request.POST
    else:
        return redirect('disney')
