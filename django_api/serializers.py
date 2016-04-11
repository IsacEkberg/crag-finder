from rest_framework import serializers
from .models import Area, RockFace, Route, Parking, Club, AreaImage, RockFaceImage


class AreaSerializer(serializers.ModelSerializer):
    rockfaces = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parking = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Area
        fields = (
            'id',
            'name',
            'rockfaces',
            'parking',
            'short_description',
            'long_description',
            'road_description',
            'image')
        read_only_fields = ('id', 'name')


class RockFaceSerializer(serializers.ModelSerializer):
    routes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = RockFace
        fields = (
            'id',
            'name',
            'routes',
            'area',
            'geo_data',
            'short_description',
            'long_description',
            'image')


class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = ('id', 'position')


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = (
            'id',
            'name',
            'rock_face',
            'grade',
            'type',
            'short_description',
            'first_ascent_name',
            'first_ascent_year',
            'length')


class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ('id', 'name', 'address', 'email', 'info')


class AreaImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = AreaImage
        fields = ('id', 'image', 'area')


class RockFaceImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RockFaceImage
        fields = ('id', 'image', 'rockface')
