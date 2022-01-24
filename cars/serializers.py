from rest_framework import serializers

from cars.models import Car, CarRating


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRating
