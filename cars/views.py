from django.db.models import Count
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView

from cars.models import Car, CarRating
from cars.serializers import CarSerializer, CarRatingSerializer, CarPopularitySerializer


class CarsViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class CarRatingCreateAPIView(CreateAPIView):
    serializer_class = CarRatingSerializer
    queryset = CarRating.objects.all()


class PopularCarListAPIView(ListAPIView):
    serializer_class = CarPopularitySerializer

    def get_queryset(self):
        return Car.objects.all().annotate(rating_count=Count('ratings')).order_by('-rating_count')
