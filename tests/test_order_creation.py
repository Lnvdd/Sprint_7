import pytest
import allure
from api.order_api import OrderAPI


@allure.feature('Создание заказа')
@allure.story('Параметры заказа')
class TestOrderCreation:

    @allure.title('Создание заказа с цветом: {color_name}')
    @allure.description('Проверка создания заказа с различными вариантами цвета')
    @allure.severity("critical")
    @pytest.mark.parametrize(
        "colors,color_name",
        [
            (["BLACK"], "Один цвет BLACK"),
            (["GREY"], "Один цвет GREY"),
            (["BLACK", "GREY"], "Оба цвета"),
            ([], "Без цвета"),
        ],
    )
    def test_create_order_with_colors(self, colors, color_name):
        order_api = OrderAPI()

        with allure.step(f'Создать заказ ({color_name})'):
            response = order_api.create_order(
                first_name="Тест",
                last_name="Курьер",
                address="Москва, Тестовая 1",
                metro_station=1,
                phone="+79990001122",
                rent_time=3,
                delivery_date="2025-12-31",
                comment="комментарий",
                color=colors
            )

        with allure.step('Проверить 201'):
            assert response.status_code == 201

        with allure.step('Проверить наличие track'):
            body = response.json()
            assert "track" in body
            allure.attach(str(body), name="Response", attachment_type=allure.attachment_type.JSON)