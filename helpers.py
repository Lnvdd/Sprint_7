import requests
import random
import string

class APIClient:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

class CourierAPI:
    def __init__(self):
        self.base_url = APIClient.BASE_URL

    def create_courier(self, login, password, first_name):
        payload = {"login": login, "password": password, "firstName": first_name}
        return requests.post(f"{self.base_url}/api/v1/courier", json=payload)

    def login_courier(self, login, password):
        payload = {"login": login, "password": password}
        return requests.post(f"{self.base_url}/api/v1/courier/login", json=payload)

    def delete_courier(self, courier_id):
        return requests.delete(f"{self.base_url}/api/v1/courier/{courier_id}")

class OrderAPI:
    def __init__(self):
        self.base_url = APIClient.BASE_URL

    def create_order(self, first_name, last_name, address, metro_station,
                     phone, rent_time, delivery_date, comment, color):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
            "color": color
        }
        return requests.post(f"{self.base_url}/api/v1/orders", json=payload)

    def get_orders(self):
        return requests.get(f"{self.base_url}/api/v1/orders")