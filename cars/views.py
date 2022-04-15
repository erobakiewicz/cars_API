from django.db.models import Count
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView

from cars.models import Car, CarRating
from cars.serializers import CarSerializer, CarRatingSerializer, CarPopularitySerializer, CreateCarSerializer


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
    pass
