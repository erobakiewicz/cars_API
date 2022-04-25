from rest_framework import serializers

from cars.models import Car, CarRating
from cars.services.vehicle_api import VehicleAPICConnector


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.ReadOnlyField()
    rates_number = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'avg_rating', 'rates_number']

    def validate_make(self, value):
        return value.lower().capitalize()

    def validate_model(self, value):
        return value.lower().capitalize()


class CreateCarSerializer(CarSerializer):

    def create(self, validated_data):
        """
        Serializer method takes request params "make" and "model" and pass them to VehicleAPIConnector.
        VehicleAPI connector make request to external API with those params and checks if object matching criteria
        exists. If so Car object is created if not returns response with error message.
        """
        connector = VehicleAPICConnector(validated_data)
        data = connector.get_vehicle_data()
        new_car = connector.validate_vehicle_data(data)
        obj = Car.objects.create(**new_car)
        obj.save()
        return obj


class CarRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRating
        fields = ['rating', 'car_id']


class CarPopularitySerializer(serializers.ModelSerializer):
    rates_number = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'rates_number']
