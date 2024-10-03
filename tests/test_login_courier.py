import pytest
import requests
from conftest import BASE_URL, create_courier
import allure


class TestCourierLogin:
    @allure.title("Успешная авторизация курьера с получением соответствующего документации ответа")
    def test_login_courier_success(self, create_courier):
        payload = {
            "login": create_courier["login"],
            "password": create_courier["password"]
        }
        response = requests.post(f'{BASE_URL}courier/login', json=payload)
        assert response.status_code == 200, "Ошибка при авторизации курьера"
        assert "id" in response.json(), "Ответ не содержит ID курьера"
        assert isinstance(response.json()["id"], int), "ID курьера должен быть числом"

    # Этот тест сделан с учётом того, что документация отличается от фактической работы сервиса
    # (тест сделан под фактическую работу сервиса)
    @allure.title("Авторизация курьера без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, create_courier, missing_field):
        payload = {
            "login": create_courier["login"],
            "password": create_courier["password"]
        }
        payload.pop(missing_field)

        response = requests.post(f'{BASE_URL}courier/login', json=payload)

        if missing_field == "password":
            assert response.status_code == 504, "Ожидалась ошибка 504 при отсутствии поля password"

            assert response.text == "Service unavailable", "Ожидалось сообщение 'Service unavailable' для ошибки 504"
        else:
            assert response.status_code == 400, f"Должен вернуться код 400 при отсутствии поля {missing_field}"

            assert response.json().get(
                "message") == "Недостаточно данных для входа", "Сообщение об ошибке должно быть корректным"

    @allure.title("Авторизация курьера с неверным логин или пароль")
    @pytest.mark.parametrize("wrong_field, wrong_value", [
        ("login", "wrong_login"),
        ("password", "wrong_password")
    ])
    def test_login_wrong_credentials(self, create_courier, wrong_field, wrong_value):
        payload = {"login": create_courier["login"], "password": create_courier["password"], wrong_field: wrong_value}

        response = requests.post(f'{BASE_URL}courier/login', json=payload)
        assert response.status_code == 404, f"Должен вернуться код 404 при неверном {wrong_field}"
        assert response.json().get("message") == "Учетная запись не найдена", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Авторизация с несуществующим пользователем")
    def test_login_nonexistent_user(self):
        payload = {
            "login": "nonexistent_login",
            "password": "nonexistent_password"
        }
        response = requests.post(f'{BASE_URL}courier/login', json=payload)
        assert response.status_code == 404, "Должен вернуться код 404 при авторизации несуществующего пользователя"
        assert response.json().get("message") == "Учетная запись не найдена", \
            "Сообщение об ошибке должно быть корректным"
