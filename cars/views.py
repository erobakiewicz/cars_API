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
    def post(self, request):
        connector = VehicleAPICConnector(request.data)
        list_of_cars = connector.get_vehicle_models_by_make_data()
        serialized_list_of_cars = []
        for car in list_of_cars:
            serialized_list_of_cars.append(car)
        return Response(status=status.HTTP_200_OK, data=serialized_list_of_cars)
