from rest_framework.exceptions import APIException
import requests

BASE_URL = 'https://vpic.nhtsa.dot.gov/api/'


class VehicleAPICConnectorError(APIException):
    pass


class VehicleAPICConnector:

    def __init__(self, make, model):
        self.make = make
        self.model = model

    def get_vehicle_data(self):
        response = requests.get(
            url=f'{BASE_URL}vehicles/getmodelsformake/{self.make}?format=json'
        )
        print(response)
