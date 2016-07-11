import json

import random
import string

from django.http import JsonResponse
from django.contrib.admin import filters
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
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


# TODO: Finish view.
@transaction.atomic
def save_route_nodes(request, pk):
    rockface_image = get_object_or_404(RockFaceImage, pk=pk)
    old_nodes = RouteNode.objects.filter(image=rockface_image)
    # Validates if data is correct.
    # Removes old route_nodes.
    # Saves new ones.

    if request.method == 'POST':
        recieved_data = json.loads(request.body.decode('utf-8'))
        print(recieved_data)
        if len(old_nodes) == 0:
            print("no earlier nodes!")
        else:
            old_nodes.delete()

        for route_id in recieved_data:
            route = Route.objects.get(pk=route_id)  # Should probably throw exception and abort atomic transaction?

            for route_node in recieved_data[route_id]:

                node, created = RouteNode.objects.get_or_create(
                    image=rockface_image,
                    pos_x=route_node['left'],
                    pos_y=route_node['top']
                )
                route.add_route_node(node, route_node['order'])

        return HttpResponse(status=200)
    else:
        return redirect("/")
