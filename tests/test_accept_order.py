import requests
from conftest import BASE_URL, create_order, login_courier
import allure


class TestAcceptOrder:
    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, login_courier, create_order):
        courier_id = login_courier
        order_id = create_order["id"]

        accept_response = requests.put(f'{BASE_URL}orders/accept/{order_id}?courierId={courier_id}')
        assert accept_response.status_code == 200, "Должен вернуться код 200 при успешном принятии заказа"
        assert accept_response.json().get("ok") is True, "Ответ должен содержать {'ok': true}"

    @allure.title("Принятие заказа без ID курьера")
    def test_accept_order_without_courier_id(self, create_order):
        order_id = create_order["id"]

        accept_response = requests.put(f'{BASE_URL}orders/accept/{order_id}')
        assert accept_response.status_code == 400, "Должен вернуться код 400 при отсутствии ID курьера"
        assert accept_response.json().get("message") == "Недостаточно данных для поиска", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Принятие заказа с неверным ID курьера")
    def test_accept_order_invalid_courier_id(self, create_order):
        order_id = create_order["id"]

        invalid_courier_id = 999999
        accept_response = requests.put(f'{BASE_URL}orders/accept/{order_id}?courierId={invalid_courier_id}')
        assert accept_response.status_code == 404, "Должен вернуться код 404 при неверном ID курьера"
        assert accept_response.json().get("message") == "Курьера с таким id не существует", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Принятие заказа без ID заказа")
    def test_accept_order_without_order_id(self, login_courier):
        courier_id = login_courier

        accept_response = requests.put(f'{BASE_URL}orders/accept/?courierId={courier_id}')
        assert accept_response.status_code == 404, "Должен вернуться код 404 при отсутствии ID заказа"
        assert accept_response.json().get("message") == "Not Found.", "Сообщение об ошибке должно быть корректным"

    @allure.title("Принятие заказа с неверным ID заказа")
    def test_accept_order_invalid_order_id(self, login_courier):
        courier_id = login_courier
        invalid_order_id = 999999

        accept_response = requests.put(f'{BASE_URL}orders/accept/{invalid_order_id}?courierId={courier_id}')
        assert accept_response.status_code == 404, "Должен вернуться код 404 при неверном ID заказа"
        assert accept_response.json().get("message") == "Заказа с таким id не существует", \
            "Сообщение об ошибке должно быть корректным"
