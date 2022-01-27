import factory.django

from cars.models import Car, CarRating


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car


class CarRatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CarRating
