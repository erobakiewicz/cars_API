import pytest

from cars.models import Car


@pytest.fixture()
def car():
    return Car.objects.create(id=1, make="Fiat", model="500")
