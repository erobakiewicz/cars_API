from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cars.models import Car, CarRating
from cars.serializers import CarSerializer, CarRatingSerializer, CarPopularitySerializer, CreateCarSerializer
from cars.services.vehicle_api import VehicleAPICConnector


class CarsViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCarSerializer
        else:
            return CarSerializer


class CarRatingCreateAPIView(CreateAPIView):
    serializer_class = CarRatingSerializer
    queryset = CarRating.objects.all()


class PopularCarListAPIView(ListAPIView):
    serializer_class = CarPopularitySerializer

    def get_queryset(self):
        return Car.objects.all().annotate(rating_count=Count('ratings')).order_by('-rating_count')


class AllCarsByMakeAPIView(APIView):
    """
    Allows to see all car models by specifc make.
    Optional if "create" param is passed it creates Car objects from first 10 endries in API response.
    """

    def post(self, request):
        connector = VehicleAPICConnector(request.data)
        list_of_cars = connector.get_vehicle_models_by_make_data()
        formatted_list_of_cars = connector.validate_vehicles_by_make_data(list_of_cars)
        length = 10 if len(formatted_list_of_cars) >= 10 else len(formatted_list_of_cars)
        cars_to_create = formatted_list_of_cars[:length]
        if request.data.get("create") == "True":
            created_cars_ids = []
            for car in cars_to_create:
                car = CarSerializer(data=car)
                if car.is_valid():
                    created_car, created = Car.objects.get_or_create(**car.validated_data)
                    if created:
                        car_id = created_car.id
                        created_cars_ids.append(car_id)
            serializer = CarSerializer(data=Car.objects.filter(id__in=created_cars_ids), many=True)
            serializer.is_valid()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        serializer = CarSerializer(data=cars_to_create, many=True)
        serializer.is_valid()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
