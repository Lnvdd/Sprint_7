import pytest
from api.courier_api import CourierAPI
from utils.data import generate_random_string

@pytest.fixture
def courier_api():
    return CourierAPI()

@pytest.fixture
def courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

@pytest.fixture
def created_courier(courier_api, courier_data):
    response = courier_api.create_courier(
        courier_data["login"],
        courier_data["password"],
        courier_data["firstName"]
    )
    
    courier_id = None
    if response.status_code == 201:
        login_resp = courier_api.login_courier(
            courier_data["login"],
            courier_data["password"]
        )
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
    
    yield {"data": courier_data, "id": courier_id}
    
    if courier_id:
        courier_api.delete_courier(courier_id)