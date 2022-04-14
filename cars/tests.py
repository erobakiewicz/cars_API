import json
from unittest.mock import patch, MagicMock

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cars.factories import CarFactory, CarRatingFactory
from cars.models import Car
from cars.services.vehicle_api import NO_MAKE_ERROR_MSG, NO_MODEL_ERROR_MSG

import pytest

pytestmark = pytest.mark.django_db


# cars app general tests

def test_cars_should_return_empty_list(client):
    response = client.get(reverse("cars:cars-list"))
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == []


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


class CarsTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.car = CarFactory(make="Fiat", model="500")
        cls.get_vehicle_data_return_value = {'Results': [
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}

    def test_carviewset_list(self):
        response = self.client.get(reverse("cars:cars-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('id'), self.car.id)

    def test_carviewset_detail(self):
        response = self.client.get(reverse("cars:cars-detail", args={self.car.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('id'), self.car.id)

    def test_carviewset_delete(self):
        response = self.client.delete(reverse("cars:cars-detail", args={self.car.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Car.objects.get(id=self.car.id)

    @patch('cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data')
    def test_carviewset_create_car(self, mock_vehicle_api):
        mock_vehicle_api.return_value = self.get_vehicle_data_return_value
        response = self.client.post(
            reverse("cars:cars-list"),
            data={
                "make": "Fiat",
                "model": "Freemont"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Car.objects.get(id=response.json().get('id')))

    @patch('cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data')
    def test_alertviews_cannot_create_car_for_non_existing_make(self, mock_vehicle_api):
        mock_vehicle_api.return_value = {'Results': []}
        response = self.client.post(
            reverse("cars:cars-list"),
            data={
                "make": "Non-existo",
                "model": "Nullus"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], NO_MAKE_ERROR_MSG)

    @patch('cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data')
    def test_alertviews_cannot_create_car_for_non_existing_model(self, mock_vehicle_api):
        mock_vehicle_api.return_value = self.get_vehicle_data_return_value
        response = self.client.post(
            reverse("cars:cars-list"),
            data={
                "make": "Fiat",
                "model": "Nullus"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], NO_MODEL_ERROR_MSG)


class CarRatingTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.car = CarFactory(make="Fiat", model="500")

    def test_cannot_rate_non_existing_car(self):
        test_car = CarFactory()
        test_car_id = test_car.id
        test_car.delete()
        response = self.client.post(
            reverse('cars:rate'),
            data={
                "car_id": test_car_id,
                "rating": 4
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_rating(self):
        response = self.client.post(
            reverse('cars:rate'),
            data={
                "car_id": self.car.id,
                "rating": 5

            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rating_out_of_range(self):
        response = self.client.post(
            reverse('cars:rate'),
            data={
                "car_id": self.car.id,
                "rating": 7

            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
