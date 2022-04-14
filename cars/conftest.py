import pytest

from cars.models import Car, CarRating


@pytest.fixture()
def car() -> Car:
    return Car.objects.create(id=1, make="Fiat", model="500")


@pytest.fixture()
def rating() -> CarRating:
    return CarRating.objects.create()
