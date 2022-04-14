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
        Method performs request to external API to check if requested car make exists.
        Returns json response with list of models or empty list if there is no such car make.
        """
        try:
            response = requests.get(
                url=f'{BASE_URL}vehicles/getmodelsformake/{self.make}?format=json',
            )
        except socket.error as e:
            raise VehicleAPICConnectionError(e)
        return response.json()

    def validate_vehicle_data(self, response):
        if not response.get('Results'):
            raise ValidationError(NO_MAKE_ERROR_MSG)
        formatted_result = self.formatted_vehicle_data(response.get('Results'))
        return formatted_result

    def get_vehicle_models_by_make_data(self):
        """
        Method performs request to external API to get a list of models of given make.
        Returns json response with a list of models of given make or empty list if there is no such car make.
        """
        try:
            response = requests.get(
                url=f'{BASE_URL}/vehicles/GetModelsForMake/{self.make}?format=json'
            )
        except socket.error as e:
            raise VehicleAPICConnectionError(e)
        return response.json()

    def formatted_vehicle_data(self, result_list):
        """
        Takes response from get_vehicle_data() method and checks if list of models is not empty.
        If list is empty returns response ValidationError - no such car make.
        If list is not empty checks if car model passed in car_data variable is present in the list of models.
        If it's present it returns dict which contain car data, else returns response ValidationError - no such model.
        """
        if result := [result for result in result_list if result['Model_Name'] == self.model]:
            formatted_result = result[0]
            if formatted_result.get("Make_ID"):
                formatted_result.pop("Make_ID")
            if formatted_result.get("Model_ID"):
                formatted_result.pop("Model_ID")
            formatted_result["make"] = formatted_result.pop("Make_Name")
            formatted_result["model"] = formatted_result.pop("Model_Name")
            return formatted_result
        else:
            raise ValidationError(NO_MODEL_ERROR_MSG)
