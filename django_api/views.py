from django.contrib.admin import filters
from django.db.models import Q
from rest_framework import viewsets, filters

from .models import Area, Parking, Route, RockFace, Club, AreaImage, RockFaceImage, APPROVED, BEING_REVIEWED_DELETE
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
    queryset = Club.objects.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class AreaImageViewSet(viewsets.ModelViewSet):
    serializer_class = AreaImageSerializer
    queryset = AreaImage.objects.all()


class RockFaceImageViewSet(viewsets.ModelViewSet):
    serializer_class = RockFaceImageSerializer
    queryset = RockFaceImage.objects.all()
