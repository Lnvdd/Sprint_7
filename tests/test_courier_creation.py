import allure
from api.courier_api import CourierAPI
from utils.data import generate_random_string


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
            assert response.status_code == 201

        with allure.step('Проверить ok: true'):
            body = response.json()
            assert body.get("ok") is True
            allure.attach(str(body), name="Response", attachment_type=allure.attachment_type.JSON)

        login_resp = courier_api.login_courier(courier_data["login"], courier_data["password"])
        if login_resp.status_code == 200:
            courier_id = login_resp.json().get("id")
            courier_api.delete_courier(courier_id)

    @allure.title('Нельзя создать двух одинаковых курьеров')
    @allure.description('Проверка, что нельзя создать курьера с существующим логином')
    @allure.severity("critical")
    def test_create_duplicate_courier(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Попытка создать курьера с существующим логином'):
            response = courier_api.create_courier(data["login"], data["password"], data["firstName"])

        with allure.step('Проверить код ошибки 409'):
            assert response.status_code == 409
            body = response.json()
            assert "message" in body
            allure.attach(response.text, name="Error", attachment_type=allure.attachment_type.TEXT)

    @allure.title('Нельзя создать курьера без логина')
    @allure.description('Проверка создания курьера без поля login')
    @allure.severity("normal")
    def test_create_courier_without_login(self, courier_api, courier_data):
        with allure.step('Отправить запрос без login'):
            response = courier_api.create_courier("", courier_data["password"], courier_data["firstName"])

        with allure.step('Проверить ошибку 400'):
            assert response.status_code == 400
            body = response.json()
            assert "message" in body
            assert body["message"]
            allure.attach(str(body), name="Error", attachment_type=allure.attachment_type.JSON)

    @allure.title('Нельзя создать курьера без пароля')
    @allure.description('Проверка создания курьера без поля password')
    @allure.severity("normal")
    def test_create_courier_without_password(self, courier_api, courier_data):
        with allure.step('Отправить запрос без password'):
            response = courier_api.create_courier(courier_data["login"], "", courier_data["firstName"])

        with allure.step('Проверить ошибку 400'):
            assert response.status_code == 400
            body = response.json()
            assert "message" in body
            assert body["message"]
            allure.attach(str(body), name="Error", attachment_type=allure.attachment_type.JSON)

    @allure.title('Нельзя создать курьера с существующим логином')
    @allure.description('Проверка ошибки при создании с уже существующим логином')
    @allure.severity("critical")
    def test_create_courier_with_existing_login(self, courier_api, created_courier):
        data = created_courier["data"]
        new_password = generate_random_string()

        with allure.step('Попытка создать с существующим логином'):
            response = courier_api.create_courier(data["login"], new_password, "John")

        with allure.step('Проверить код 409'):
            assert response.status_code == 409
            body = response.json()
            assert "message" in body