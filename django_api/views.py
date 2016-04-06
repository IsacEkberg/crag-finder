from django.contrib.admin import filters
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
import django_filters

from .models import Area, Parking, Route, RockFace
from .serializers import AreaSerializer, RockFaceSerializer, ParkingSerializer, RouteSerializer


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