import json
from unittest.mock import patch, MagicMock
import pytest
from django.urls import reverse
from rest_framework import status

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

def test_popular_car_list_returns_empty_list(client):
    response = client.get(reverse("cars:popular"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


# tests for get car models by make
@patch(
    'cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_models_by_make_data',
    MagicMock(
        return_value={'Results': [
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}
    )
)
def test_all_cars_by_make_returns_list_of_cars(client):
    response = client.post(
        reverse("cars:cars_by_make"),
        data={
            "make": "FIAT"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'make': 'Fiat', 'model': '500'}, {'make': 'Fiat', 'model': 'Freemont'}, {'make': 'Fiat', 'model': 'Ducato'}
    ]


@patch(
    'cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_models_by_make_data',
    MagicMock(
        return_value={'Results': [
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}
    )
)
def test_all_cars_by_make_creates_three_objs_from_response(client):
    response = client.post(
        reverse("cars:cars_by_make"),
        data={
            "make": "FIAT",
            "create": "True"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {'id': 2, 'make': 'Fiat', 'model': '500', 'avg_rating': 0, 'rates_number': 0},
        {'id': 3, 'make': 'Fiat', 'model': 'Freemont', 'avg_rating': 0, 'rates_number': 0},
        {'id': 4, 'make': 'Fiat', 'model': 'Ducato', 'avg_rating': 0, 'rates_number': 0}
    ]


@patch(
    'cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_models_by_make_data',
    MagicMock(
        return_value={'Results': [
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
            {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}
    )
)
def test_all_cars_by_make_create_objects_from_response_action(client):
    client.force_login(client)
    response = client.get(reverse("admin:cars_car_changelist"))
    print(response.__dict__)
    assert response.status_code == status.HTTP_200_OK
