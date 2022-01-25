from unittest.mock import patch

from django.db.models import Max, Count
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from cars.models import Car, CarRating


class CarsTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.car = Car.objects.create(make="Fiat", model="500")
        cls.get_vehicle_data_return_value = {'Count': 10, 'Message': 'Response returned successfully',
                                             'SearchCriteria': 'Make:Fiat', 'Results': [
                {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 2055, 'Model_Name': '500'},
                {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 3490, 'Model_Name': 'Freemont'},
                {'Make_ID': 492, 'Make_Name': 'FIAT', 'Model_ID': 25128, 'Model_Name': 'Ducato'}]}

    def test_carviewset_list(self):
        response = self.client.get(reverse("cars:cars-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_carviewset_detail(self):
        response = self.client.get(reverse("cars:cars-detail", args={self.car.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_carviewset_delete(self):
        response = self.client.delete(reverse("cars:cars-detail", args={self.car.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

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

    @patch('cars.services.vehicle_api.VehicleAPICConnector.get_vehicle_data')
    def test_alertviews_cannot_create_car_for_non_existing_make(self, mock_vehicle_api):
        mock_vehicle_api.return_value = self.get_vehicle_data_return_value
        response = self.client.post(
            reverse("cars:cars-list"),
            data={
                "make": "Non-existo",
                "model": "Nullus"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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


class CarRatingTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.car = Car.objects.create(make="Fiat", model="500")

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
        cls.client = APIClient()
        cls.car1 = Car.objects.create(make="Fiat", model="500")
        cls.car2 = Car.objects.create(make="Opel", model="Astra")
        cls.car1_rate1 = CarRating.objects.create(car_id=cls.car1, rating=5)
        cls.car1_rate2 = CarRating.objects.create(car_id=cls.car1, rating=5)
        cls.car2_rate1 = CarRating.objects.create(car_id=cls.car2, rating=5)
        cls.car2_rate2 = CarRating.objects.create(car_id=cls.car2, rating=5)
        cls.car2_rate3 = CarRating.objects.create(car_id=cls.car1, rating=5)

    def test_get_most_popular_car_first_in_response_data_list_of_objects(self):
        response = self.client.get(reverse('cars:popular'))
        highest_num_of_ratings = \
            Car.objects.all().annotate(rating_count=Count('ratings')).aggregate(Max('rating_count'))[
                'rating_count__max']
        self.assertEqual(response.json()[0].get('rates_number'), highest_num_of_ratings)
