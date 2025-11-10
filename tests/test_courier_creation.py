import pytest
import allure
from helpers import CourierAPI, APIClient


@allure.feature('Создание курьера')
@allure.story('API тестирование курьеров')
class TestCourierCreation:

    @allure.title('Курьера можно создать')
    @allure.description('Проверка успешного создания курьера с валидными данными')
    @allure.severity("critical")
    def test_create_courier_success(self, courier_api, courier_data):
        with allure.step('Отправить запрос на создание курьера'):
            response = courier_api.create_courier(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        with allure.step('Проверить код ответа 201'):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        with allure.step('Проверить, что ответ содержит ok: true'):
            body = response.json()
            assert body.get("ok") is True, "Ответ должен содержать ok: true"
            allure.attach(str(body), name="Response Body", attachment_type=allure.attachment_type.JSON)

    @allure.title('Нельзя создать двух одинаковых курьеров')
    @allure.description('Проверка, что нельзя создать курьера с существующим логином')
    @allure.severity("critical")
    def test_create_duplicate_courier(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Попытка создать курьера с существующим логином'):
            response = courier_api.create_courier(data["login"], data["password"], data["firstName"])

        with allure.step('Проверить код ошибки 409'):
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"
            allure.attach(response.text, name="Error Response", attachment_type=allure.attachment_type.TEXT)

    @allure.title('Нельзя создать курьера без логина')
    @allure.description('Проверка создания курьера без обязательного поля login')
    @allure.severity("normal")
    def test_create_courier_without_login(self, courier_api, courier_data):
        with allure.step('Отправить запрос без поля login'):
            response = courier_api.create_courier("", courier_data["password"], courier_data["firstName"])

        with allure.step('Проверить ошибку 400'):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

    @allure.title('Нельзя создать курьера без пароля')
    @allure.description('Проверка создания курьера без обязательного поля password')
    @allure.severity("normal")
    def test_create_courier_without_password(self, courier_api, courier_data):
        with allure.step('Отправить запрос без поля password'):
            response = courier_api.create_courier(courier_data["login"], "", courier_data["firstName"])

        with allure.step('Проверить ошибку 400'):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

    @allure.title('Нельзя создать курьера с существующим логином')
    @allure.description('Проверка, что при создании курьера с уже существующим логином возвращается ошибка')
    @allure.severity("critical")
    def test_create_courier_with_existing_login(self, courier_api, created_courier):
        data = created_courier["data"]
        new_password = APIClient.generate_random_string(10)

        with allure.step('Попытка создать курьера с существующим логином (другие поля изменены)'):
            response = courier_api.create_courier(data["login"], new_password, "John")

        with allure.step('Проверить код ошибки 409'):
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"