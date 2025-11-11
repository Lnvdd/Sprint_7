import allure
from api.courier_api import CourierAPI
from utils.data import generate_random_string


@allure.feature('Авторизация курьера')
@allure.story('API логин курьеров')
class TestCourierLogin:

    @allure.title('Курьер может авторизоваться')
    @allure.description('Проверка успешной авторизации')
    @allure.severity("critical")
    def test_courier_can_login(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Отправить запрос на логин'):
            response = courier_api.login_courier(data["login"], data["password"])

        with allure.step('Проверить код 200'):
            assert response.status_code == 200

        with allure.step('Проверить наличие id'):
            body = response.json()
            assert "id" in body
            allure.attach(str(body), name="Response", attachment_type=allure.attachment_type.JSON)

    @allure.title('Для авторизации нужны все обязательные поля')
    @allure.description('Проверка на отсутствие обязательных полей')
    @allure.severity("normal")
    def test_login_requires_all_fields(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Попытка логина без пароля'):
            resp = courier_api.login_courier(data["login"], "")
            assert resp.status_code == 400
            body = resp.json()
            assert "message" in body and body["message"]
            allure.attach(str(body), name="Error", attachment_type=allure.attachment_type.JSON)

        with allure.step('Попытка логина без логина'):
            resp = courier_api.login_courier("", data["password"])
            assert resp.status_code == 400
            body = resp.json()
            assert "message" in body and body["message"]
            allure.attach(str(body), name="Error", attachment_type=allure.attachment_type.JSON)

    @allure.title('Ошибка при неправильном логине')
    @allure.description('При неверном логине возвращается 404')
    @allure.severity("normal")
    def test_wrong_login(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Отправить неправильный логин'):
            resp = courier_api.login_courier("wronglogin", data["password"])
            assert resp.status_code == 404
            body = resp.json()
            assert "message" in body

    @allure.title('Ошибка при неправильном пароле')
    @allure.description('При неверном пароле возвращается 404')
    @allure.severity("normal")
    def test_wrong_password(self, courier_api, created_courier):
        data = created_courier["data"]

        with allure.step('Отправить неправильный пароль'):
            resp = courier_api.login_courier(data["login"], "wrongpass")
            assert resp.status_code == 404
            body = resp.json()
            assert "message" in body

    @allure.title('Ошибка для несуществующего пользователя')
    @allure.description('Логин с фейковыми учётными данными')
    @allure.severity("normal")
    def test_non_existent_user(self, courier_api):
        fake_login = generate_random_string()
        fake_password = generate_random_string()

        with allure.step('Отправить фейковые данные'):
            resp = courier_api.login_courier(fake_login, fake_password)
            assert resp.status_code == 404
            body = resp.json()
            assert "message" in body