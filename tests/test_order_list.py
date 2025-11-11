import allure
from api.order_api import OrderAPI


@allure.feature('Список заказов')
@allure.story('Получение заказов')
class TestOrderList:

    @allure.title('В ответ возвращается список заказов')
    @allure.description('Проверка, что API возвращает список заказов')
    @allure.severity("critical")
    def test_get_orders_returns_list(self):
        order_api = OrderAPI()

        with allure.step('GET /api/v1/orders'):
            response = order_api.get_orders()

        with allure.step('Проверить 200'):
            assert response.status_code == 200

        with allure.step('Проверить orders в теле'):
            body = response.json()
            assert "orders" in body
            assert isinstance(body["orders"], list)
            allure.attach(str(body), name="Response", attachment_type=allure.attachment_type.JSON)

    @allure.title('Список заказов не пустой')
    @allure.description('Проверка, что возвращается непустой список')
    @allure.severity("normal")
    def test_orders_list_not_empty(self):
        order_api = OrderAPI()
        response = order_api.get_orders()
        assert response.status_code == 200
        body = response.json()
        assert len(body["orders"]) > 0

    @allure.title('Каждый заказ содержит обязательные поля')
    @allure.description('Проверка структуры данных заказа')
    @allure.severity("normal")
    def test_order_structure(self):
        order_api = OrderAPI()
        response = order_api.get_orders()
        assert response.status_code == 200
        
        orders = response.json()["orders"]
        if orders:
            first = orders[0]
            expected = ["id", "firstName", "lastName", "address", "phone"]
            missing = [f for f in expected if f not in first]
            assert not missing
            allure.attach(str(first), name="Order", attachment_type=allure.attachment_type.JSON)