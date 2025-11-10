import pytest
import allure
from helpers import OrderAPI


@allure.feature('Создание заказа')
@allure.story('Параметры заказа')
class TestOrderCreation:

    @allure.title('Создание заказа с цветом: {color}')
    @allure.description('Проверка создания заказа с различными вариантами цвета')
    @allure.severity("critical")
    @pytest.mark.parametrize(
        "color",
        [
            (["BLACK"], "Один цвет BLACK"),
            (["GREY"], "Один цвет GREY"),
            (["BLACK", "GREY"], "Оба цвета"),
            ([], "Без цвета"),
        ],
    )
    def test_create_order_with_colors(self, color):
        color_list, color_name = color
        order_api = OrderAPI()

        with allure.step(f'Создать заказ с цветом: {color_name}'):
            response = order_api.create_order(
                first_name="Тест",
                last_name="Курьер",
                address="Москва, Тестовая 1",
                metro_station=1,
                phone="+79990001122",
                rent_time=3,
                delivery_date="2025-12-31",
                comment="комментарий",
                color=color_list
            )

        with allure.step('Проверить 201'):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

        with allure.step('Проверить, что в ответе есть track'):
            body = response.json()
            assert "track" in body, "Ответ должен содержать поле track"
            allure.attach(str(body), name="Order Response", attachment_type=allure.attachment_type.JSON)

    @allure.title('Можно указать один цвет BLACK')
    @allure.description('Проверка создания заказа с одним цветом BLACK')
    @allure.severity("normal")
    def test_create_order_with_black_color(self):
        order_api = OrderAPI()
        response = order_api.create_order(
            first_name="Иван",
            last_name="Иванов",
            address="Москва, Ленина 10",
            metro_station=1,
            phone="+79991234567",
            rent_time=3,
            delivery_date="2025-12-20",
            comment="Доставка",
            color=["BLACK"]
        )
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title('Можно указать один цвет GREY')
    @allure.description('Проверка создания заказа с одним цветом GREY')
    @allure.severity("normal")
    def test_create_order_with_grey_color(self):
        order_api = OrderAPI()
        response = order_api.create_order(
            first_name="Петр",
            last_name="Петров",
            address="СПб, Невский 5",
            metro_station=2,
            phone="+79997654321",
            rent_time=7,
            delivery_date="2025-12-25",
            comment="Позвонить",
            color=["GREY"]
        )
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title('Можно указать оба цвета')
    @allure.description('Проверка создания заказа с обоими цветами')
    @allure.severity("normal")
    def test_create_order_with_both_colors(self):
        order_api = OrderAPI()
        response = order_api.create_order(
            first_name="Сидор",
            last_name="Сидоров",
            address="Казань, Баумана 15",
            metro_station=3,
            phone="+79993456789",
            rent_time=2,
            delivery_date="2025-12-15",
            comment="Быстро",
            color=["BLACK", "GREY"]
        )
        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title('Можно не указывать цвет')
    @allure.description('Проверка создания заказа без указания цвета')
    @allure.severity("normal")
    def test_create_order_without_color(self):
        order_api = OrderAPI()
        response = order_api.create_order(
            first_name="Анна",
            last_name="Аннова",
            address="Екатеринбург, Малышева 20",
            metro_station=5,
            phone="+79998765432",
            rent_time=1,
            delivery_date="2025-12-10",
            comment="У двери",
            color=[]
        )
        assert response.status_code == 201
        assert "track" in response.json()