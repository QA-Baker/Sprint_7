import requests
from conftest import BASE_URL
import allure


class TestListOrders:
    @allure.title("Получение списка заказов")
    def test_list_orders_returns_orders(self):
        response = requests.get(f'{BASE_URL}orders?limit=5')

        assert response.status_code == 200, "Запрос на получение списка заказов должен возвращать код 200"

        response_json = response.json()
        assert "orders" in response_json, "Ответ должен содержать поле 'orders'"
        assert isinstance(response_json["orders"], list), "Поле 'orders' должно быть списком"

        assert len(response_json["orders"]) > 0, "Список заказов должен содержать хотя бы один заказ"
