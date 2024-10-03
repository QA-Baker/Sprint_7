import pytest
import requests
from conftest import BASE_URL
import allure


class TestCreateOrder:
    @pytest.mark.parametrize("color", [
        (["BLACK"]),  # Один цвет - BLACK
        (["GREY"]),  # Один цвет - GREY
        (["BLACK", "GREY"]),  # Оба цвета
        ([])  # Без цвета
    ])
    @allure.title("Проверка создания заказа")
    def test_create_order_with_various_colors(self, color):
        order_data = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "ул. Тестовая, 1",
            "metroStation": 4,
            "phone": "+7 999 999 99 99",
            "rentTime": 5,
            "deliveryDate": "2024-01-01",
            "comment": "Тестовый заказ",
            "color": color
        }
        response = requests.post(f'{BASE_URL}orders', json=order_data)
        assert response.status_code == 201, "Должен вернуться код 201 при успешном создании заказа"
        assert "track" in response.json(), "Ответ должен содержать поле 'track'"
        assert isinstance(response.json()["track"], int), "Поле 'track' должно быть числом"
