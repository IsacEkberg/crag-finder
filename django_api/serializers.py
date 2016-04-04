from rest_framework import serializers
from .models import Rental, Area, RockFace, Route, Parking


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ('id', 'title', 'owner', 'city', 'type', 'image', 'bedrooms')


class AreaSerializer(serializers.ModelSerializer):
    rockfaces = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parking = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'rockfaces', 'parking')
        read_only_fields = ('id', 'name')


class RockFaceSerializer(serializers.ModelSerializer):
    routes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = RockFace
        fields = ('id', 'name', 'routes', 'area', 'geo_data')


class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = ('id', 'position')


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ('id', 'name', 'rock_face', 'grade', 'type')