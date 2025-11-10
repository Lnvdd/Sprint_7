import pytest
from helpers import CourierAPI, APIClient

@pytest.fixture
def courier_api():
    return CourierAPI()

@pytest.fixture
def courier_data():
    login = APIClient.generate_random_string(10)
    password = APIClient.generate_random_string(10)
    first_name = APIClient.generate_random_string(10)
    return {"login": login, "password": password, "firstName": first_name}

@pytest.fixture
def created_courier(courier_api, courier_data):
    response = courier_api.create_courier(
        courier_data["login"], courier_data["password"], courier_data["firstName"]
    )
    courier_id = None
    if response.status_code == 201:
        login_response = courier_api.login_courier(
            courier_data["login"], courier_data["password"]
        )
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
    yield {"data": courier_data, "id": courier_id}
    if courier_id:
        courier_api.delete_courier(courier_id)
