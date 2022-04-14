import json
from unittest.mock import patch, MagicMock
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.factories import CarFactory, CarRatingFactory
from cars.services.vehicle_api import NO_MAKE_ERROR_MSG, NO_MODEL_ERROR_MSG

pytestmark = pytest.mark.django_db


# cars app general tests

def test_cars_should_return_empty_list(client):
    response = client.get(reverse("cars:cars-list"))
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == []


@patch(
    'cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data',
    MagicMock(return_value={'Results': []})
)
def test_cannot_create_car_from_non_existing_make_raises_non_exsisting_make_error(client):
    response = client.post(
        reverse("cars:cars-list"),
        data={
            "make": "NOTING",
            "model": "None"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == NO_MAKE_ERROR_MSG


@patch(
    'cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data',
    MagicMock(
        return_value={'Results': [
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}
    )
)
def test_cannot_create_car_from_non_existing_model_raises_non_existing_model_error(client):
    response = client.post(
        reverse("cars:cars-list"),
        data={
            "make": "Fiat",
            "model": "Non-exisiting"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == NO_MODEL_ERROR_MSG


@patch(
    'cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data',
    MagicMock(
        return_value={'Results': [
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}
    )
)
def test_create_car(client):
    response = client.post(
        reverse("cars:cars-list"),
        data={'make': 'fiat', 'model': 'freemont'}
    )
    assert response.status_code == status.HTTP_201_CREATED

    assert response.json().get("model") == "Freemont"
    assert response.json().get("make") == "FIAT"


def test_get_details_of_a_car(client, car):
    response = client.get(reverse("cars:cars-detail", args={car.id}))
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("make") == car.make


def test_delete_car(client, car):
    response = client.delete(reverse("cars:cars-detail", args={car.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(reverse("cars:cars-list"))
    assert response.json() == []


# cars aoo rating tests

def test_cannot_rate_non_existing_car(client, car):
    car_id = car.id
    car.delete()
    response = client.post(
        reverse("cars:rate"),
        data={
            "car_id": car_id,
            "rating": 5
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_cannot_create_rating_out_of_range(client, car):
    response = client.post(
        reverse("cars:rate"),
        data={
            "car_id": car.id,
            "rating": 32
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("rating") == ['Ensure this value is less than or equal to 5.']


def test_create_car_rating(client, car):
    response = client.post(
        reverse("cars:rate"),
        data={
            "car_id": car.id,
            "rating": 3
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


# test for popular list


class PopularCarListTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.car1 = CarFactory(make="Fiat", model="500")
        cls.car2 = CarFactory(make="Opel", model="Astra")
        cls.car1_rate1 = CarRatingFactory(car_id=cls.car1, rating=5)
        cls.car1_rate2 = CarRatingFactory(car_id=cls.car1, rating=5)
        cls.car2_rate1 = CarRatingFactory(car_id=cls.car2, rating=5)
        cls.car2_rate2 = CarRatingFactory(car_id=cls.car2, rating=5)
        cls.car2_rate3 = CarRatingFactory(car_id=cls.car2, rating=5)

    def test_get_most_popular_car_first_in_response_data_list_of_objects(self):
        response = self.client.get(reverse('cars:popular'))
        self.assertEqual(response.json()[0].get('rates_number'), 3)
        self.assertEqual(response.json()[1].get('rates_number'), 2)
        self.assertEqual(response.json()[0].get('id'), self.car2.id)
        self.assertEqual(response.json()[1].get('id'), self.car1.id)
