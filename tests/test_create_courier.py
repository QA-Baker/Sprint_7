import pytest
import requests
from conftest import BASE_URL, create_courier
import allure


class TestCreateCourier:
    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, create_courier):
        assert all(create_courier.values()), "Курьер не был создан, одно из полей пустое"

    @allure.title("Невозможность создания двух одинаковых курьеров")
    def test_create_duplicate_courier(self, create_courier):
        payload = {
            "login": create_courier["login"],
            "password": create_courier["password"],
            "firstName": create_courier["first_name"]
        }
        response = requests.post(f'{BASE_URL}courier', json=payload)
        assert response.status_code == 409, "Должна вернуться ошибка при создании дубликата курьера"
        assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой.", \
            "Сообщение об ошибке должно соответствовать ожидаемому"

    @allure.title("Отсутствие обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field, create_courier):
        payload = {
            "login": create_courier["login"],
            "password": create_courier["password"],
        }
        payload.pop(missing_field, None)
        response = requests.post(f'{BASE_URL}courier', json=payload)
        assert response.status_code == 400, f"Должен вернуться код 400 при отсутствии поля {missing_field}"
        assert response.json().get(
            "message") == "Недостаточно данных для создания учетной записи", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Проверка правильного кода ответа и возвращаемого {'ok': true}")
    def test_create_courier_ok_response(self, create_courier):
        new_login = create_courier["login"] + "_new"
        new_password = "newpassword123"
        payload = {
            "login": new_login,
            "password": new_password,
            "firstName": create_courier["first_name"]
        }
        response = requests.post(f'{BASE_URL}courier', json=payload)
        assert response.status_code == 201, "Код ответа при успешном создании курьера должен быть 201"
        assert response.json().get("ok") is True, "Ответ должен содержать {'ok': true}"
