import pytest
import allure
from helpers import CourierAPI, APIClient


@allure.feature('Авторизация курьера')
@allure.story('API логин курьеров')
class TestCourierLogin:

    @allure.title('Курьер может авторизоваться')
    @allure.description('Проверка успешной авторизации курьера с валидными данными')
    @allure.severity("critical")
    def test_courier_can_login(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Отправить запрос на логин'):
            response = courier_api.login_courier(data["login"], data["password"])

        with allure.step('Проверить код ответа 200'):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step('Проверить наличие поля id'):
            body = response.json()
            assert "id" in body, "Ответ должен содержать поле id"
            allure.attach(str(body), name="Login Response", attachment_type=allure.attachment_type.JSON)

    @allure.title('Для авторизации нужны все обязательные поля')
    @allure.description('Нельзя авторизоваться без всех обязательных полей')
    @allure.severity("normal")
    def test_login_requires_all_fields(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Попытка логина без пароля'):
            resp = courier_api.login_courier(data["login"], "")
        with allure.step('Проверить 400'):
            assert resp.status_code == 400

        with allure.step('Попытка логина без логина'):
            resp = courier_api.login_courier("", data["password"])
        with allure.step('Проверить 400'):
            assert resp.status_code == 400

    @allure.title('Ошибка при неправильном логине')
    @allure.description('При неверном логине возвращается 404')
    @allure.severity("normal")
    def test_wrong_login(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Отправить логин с несуществующим пользователем'):
            resp = courier_api.login_courier("wronglogin", data["password"])
        with allure.step('Проверить 404'):
            assert resp.status_code == 404

    @allure.title('Ошибка при неправильном пароле')
    @allure.description('При неверном пароле возвращается 404')
    @allure.severity("normal")
    def test_wrong_password(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Отправить неправильный пароль'):
            resp = courier_api.login_courier(data["login"], "wrongpass")
        with allure.step('Проверить 404'):
            assert resp.status_code == 404

    @allure.title('Ошибка для несуществующего пользователя')
    @allure.description('Нельзя авторизоваться с фейковыми учётными данными')
    @allure.severity("normal")
    def test_non_existent_user(self, courier_api):
        fake_login = APIClient.generate_random_string(10)
        fake_password = APIClient.generate_random_string(10)

        with allure.step('Отправить логин с несуществующим пользователем'):
            resp = courier_api.login_courier(fake_login, fake_password)
        with allure.step('Проверить 404'):
            assert resp.status_code == 404