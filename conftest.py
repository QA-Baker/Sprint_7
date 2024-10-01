import pytest
import requests
from src.user import register_new_courier_and_return_login_password

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/'


# Фикстура для регистрации курьера через предоставленный метод
@pytest.fixture(scope="function")
def create_courier():
    login_pass = register_new_courier_and_return_login_password()
    assert login_pass, "Курьер не был создан"
    return {
        "login": login_pass[0],
        "password": login_pass[1],
        "first_name": login_pass[2]
    }


# Фикстура для логина курьера
@pytest.fixture
def login_courier(create_courier):
    payload = {
        "login": create_courier["login"],
        "password": create_courier["password"]
    }
    response = requests.post(f'{BASE_URL}courier/login', json=payload)
    assert response.status_code == 200, "Ошибка при логине курьера"
    return response.json()["id"]


# Фикстура для создания заказа
@pytest.fixture
def create_order():
    order_data = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "ул. Тестовая, 1",
        "metroStation": 4,
        "phone": "+7 999 999 99 99",
        "rentTime": 5,
        "deliveryDate": "2024-01-01",
        "comment": "Тестовый заказ",
        "color": ["BLACK"]
    }
    response = requests.post(f'{BASE_URL}orders', json=order_data)
    assert response.status_code == 201, "Ошибка при создании заказа"

    track = response.json().get("track")
    assert track, "Трек заказа не был получен"

    order_id_response = requests.get(f'{BASE_URL}orders/track?t={track}')
    assert order_id_response.status_code == 200, "Не удалось получить ID заказа по треку"

    order_id = order_id_response.json()["order"]["id"]
    return {
        "id": order_id,
        "track": track
    }
