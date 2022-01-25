from rest_framework import status
from rest_framework.exceptions import APIException
import requests

BASE_URL = 'https://vpic.nhtsa.dot.gov/api/'


class VehicleAPICConnectorError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class VehicleAPICConnector:

    def __init__(self, car_data):
        self.make = car_data.get("make")
        self.model = car_data.get('model')

    def get_vehicle_data(self):
        response = requests.get(
            url=f'{BASE_URL}vehicles/getmodelsformake/{self.make}?format=json',
        )
        return response.json()

    def formatted_vehicle_data(self):
        if not self.get_vehicle_data().get('Results'):
            raise VehicleAPICConnectorError("This car make doesn't exist")
        result_list = self.get_vehicle_data().get('Results')
        if result := [result for result in result_list if result['Model_Name'] == self.model]:
            return result[0]
        else:
            raise VehicleAPICConnectorError("This car model doesn't exist")
