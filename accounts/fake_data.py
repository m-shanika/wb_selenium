import requests
from .dataclasses import FDGender, FDResponse

class FakeData:
    @staticmethod
    def get(gender: FDGender):
        url = "https://api.randomdatatools.ru/"
        params = {
            "gender": gender,
            "params": "LastName,FirstName"
        }
        response = requests.get(url, params=params)
        return FDResponse(**response.json())