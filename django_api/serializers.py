from rest_framework import serializers
from .models import Area, RockFace, Route, Parking


class AreaSerializer(serializers.ModelSerializer):
    rockfaces = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parking = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'rockfaces', 'parking', 'short_description', 'long_description', 'road_description')
        read_only_fields = ('id', 'name')


class RockFaceSerializer(serializers.ModelSerializer):
    routes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = RockFace
        fields = ('id', 'name', 'routes', 'area', 'geo_data', 'short_description', 'long_description')


class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = ('id', 'position')


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ('id', 'name', 'rock_face', 'grade', 'type', 'short_description', 'first_ascent_name', 'first_ascent_year', 'length')