import socket

from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
import requests

BASE_URL = 'https://vpic.nhtsa.dot.gov/api/'
NO_MAKE_ERROR_MSG = "This car make doesn't exist"
NO_MODEL_ERROR_MSG = "This car model doesn't exist"


class VehicleAPICConnectionError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class VehicleAPICConnector:

    def __init__(self, car_data):
        self.make = car_data.get("make")
        self.model = car_data.get('model')

    def get_vehicle_data(self):
        """
        TODO COMĆ
        """
        try:
            response = requests.get(
                url=f'{BASE_URL}vehicles/getmodelsformake/{self.make}?format=json',
            )
        except socket.error as e:
            raise VehicleAPICConnectionError(e)
        return response.json()

    def formatted_vehicle_data(self):
        """
        #TODO COMĆ
        """
        if not self.get_vehicle_data().get('Results'):
            raise ValidationError(NO_MAKE_ERROR_MSG)
        result_list = self.get_vehicle_data().get('Results')
        if result := [result for result in result_list if result['Model_Name'] == self.model]:
            return result[0]
        else:
            raise ValidationError(NO_MODEL_ERROR_MSG)
