from rest_framework import serializers

from cars.models import Car, CarRating
from cars.services.vehicle_api import VehicleAPICConnector


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating']

    def create(self, validated_data):
        connector = VehicleAPICConnector(validated_data)
        new_car = connector.get_vehicle_data()
        obj = Car.objects.create(
            model=new_car.get("Model_Name"),
            make=new_car.get("Make_Name")
        )
        obj.save()
        return obj


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRating
        fields = ['rating', 'rated_car']
