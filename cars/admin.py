from django.contrib import admin
from cars.models import Car, CarRating
from cars.serializers import CarSerializer
from cars.services.vehicle_api import VehicleAPICConnector


@admin.action(description="Imports all car models by make of selected models")
def get_all_cars_by_make(modeladmin, request, queryset):
    messages = []
    car_makes = [{"make": make} for make in queryset.values_list("make", flat=True)]
    for make in car_makes:
        connector = VehicleAPICConnector(make)
        list_of_cars = connector.get_vehicle_models_by_make_data()
        formatted_list_of_cars = connector.validate_vehicles_by_make_data(list_of_cars)
        length = 10 if len(formatted_list_of_cars) >= 10 else len(formatted_list_of_cars)
        for car in formatted_list_of_cars[:length]:
            car_to_create = CarSerializer(data=car)
            if car_to_create.is_valid():
                created_car, created = Car.objects.get_or_create(**car_to_create.validated_data)
                if created:
                    messages.append(f'Created {created_car.make} {created_car.model}')
                messages.append(f'Car {created_car.make} {created_car.model} already exists')
            messages.append(car_to_create.errors)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'make',
        'model',
        'avg_rating'
    ]
    actions = [get_all_cars_by_make]


@admin.register(CarRating)
class CarRatingAdmin(admin.ModelAdmin):
    pass
