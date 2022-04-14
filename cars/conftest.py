import pytest

from cars.models import Car, CarRating


@pytest.fixture()
def car():
    return Car.objects.create(id=1, make="Fiat", model="500")


@pytest.fixture()
def rating():
    return CarRating.objects.create()
