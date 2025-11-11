import requests

class BaseClient:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"

    def __init__(self):
        self.base_url = self.BASE_URL

    def post(self, path: str, json=None, data=None):
        return requests.post(f"{self.base_url}{path}", json=json, data=data)

    def get(self, path: str, params=None):
        return requests.get(f"{self.base_url}{path}", params=params)

    def delete(self, path: str):
        return requests.delete(f"{self.base_url}{path}")