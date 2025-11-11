from api.base_client import BaseClient

class OrderAPI(BaseClient):

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
        return self.post("/api/v1/orders", json=payload)

    def get_orders(self):
        return self.get("/api/v1/orders")