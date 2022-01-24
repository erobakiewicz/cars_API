from rest_framework import viewsets

from cars.models import Car
from cars.serializers import CarSerializer


class CarsViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()