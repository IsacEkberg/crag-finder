from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Area, Parking, Route, RockFace
from .serializers import AreaSerializer, RockFaceSerializer, ParkingSerializer, RouteSerializer


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Area.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class RockFaceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RockFaceSerializer
    queryset = RockFace.objects.all()


class ParkingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ParkingSerializer
    queryset = Parking.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()