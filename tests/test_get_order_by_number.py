import requests
from conftest import BASE_URL, create_order
import allure


class TestGetOrderByNumber:
    @allure.title("Успешное получение заказа по его номеру")
    def test_get_order_success(self, create_order):
        track = create_order["track"]

        get_order_response = requests.get(f'{BASE_URL}orders/track?t={track}')
        assert get_order_response.status_code == 200, "Должен вернуться код 200 при успешном запросе"

        order_data = get_order_response.json().get("order")
        assert order_data, "Ответ должен содержать данные о заказе"
        assert order_data["track"] == track, "Track в ответе должен совпадать с запрашиваемым"

    @allure.title("Запрос без номера заказа")
    def test_get_order_without_track(self):
        get_order_response = requests.get(f'{BASE_URL}orders/track')
        assert get_order_response.status_code == 400, "Должен вернуться код 400 при запросе без номера заказа"
        assert get_order_response.json().get("message") == "Недостаточно данных для поиска", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Запрос с несуществующим номером заказа")
    def test_get_order_nonexistent_track(self):
        invalid_track = 999999

        get_order_response = requests.get(f'{BASE_URL}orders/track?t={invalid_track}')
        assert get_order_response.status_code == 404, "Должен вернуться код 404 при запросе с несуществующим треком"
        assert get_order_response.json().get("message") == "Заказ не найден", \
            "Сообщение об ошибке должно быть корректным"
