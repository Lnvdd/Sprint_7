from api.base_client import BaseClient

class CourierAPI(BaseClient):

    def create_courier(self, login, password, first_name):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return self.post("/api/v1/courier", json=payload)

    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        return self.post("/api/v1/courier/login", json=payload)

    def delete_courier(self, courier_id):
        return self.delete(f"/api/v1/courier/{courier_id}")