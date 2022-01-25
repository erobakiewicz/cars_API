from rest_framework.exceptions import APIException
import requests

BASE_URL = 'https://vpic.nhtsa.dot.gov/api/'


class VehicleAPICConnectorError(APIException):
    pass


class VehicleAPICConnector:

    def __init__(self, car_data):
        self.make = car_data.get("make")
        self.model = car_data.get('model')

    def get_vehicle_data(self):
        response = requests.get(
            url=f'{BASE_URL}vehicles/getmodelsformake/{self.make}?format=json',
        )
        result_list = response.json().get('Results')
        result = [result for result in result_list if result['Model_Name'] == self.model][0]
        if result:
            return result
        else:
            raise VehicleAPICConnectorError("This Car doesn't exist")
