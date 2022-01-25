from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.response import Response

from cars.models import Car, CarRating
from cars.services.vehicle_api import VehicleAPICConnector


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'model']

    def create(self, validated_data):
        connector = VehicleAPICConnector(validated_data)
        if new_car := connector.get_vehicle_data():
            obj = Car.objects.create(
                model=new_car.get("Model_Name"),
                make=new_car.get("Make_Name")
            )
            obj.save()
            return obj
        else:
            return Response("That car doesn't exist!")


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRating
        fields = ['rating', 'rated_car']
