import requests
from conftest import BASE_URL, login_courier
import allure


class TestDeleteCourier:
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, login_courier):
        courier_id = login_courier

        delete_response = requests.delete(f'{BASE_URL}courier/{courier_id}')
        assert delete_response.status_code == 200, "Должен вернуться код 200 при успешном удалении курьера"
        assert delete_response.json().get("ok") is True, "Ответ должен содержать {'ok': true}"

    @allure.title("Попытка удаления курьера без ID")
    def test_delete_courier_without_id(self):
        delete_response = requests.delete(f'{BASE_URL}courier/')
        assert delete_response.status_code == 404, "Должен вернуться код 404 при удалении без указания ID"
        assert delete_response.json().get("message") == "Not Found.", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Попытка удаления курьера с несуществующим ID")
    def test_delete_courier_nonexistent_id(self):
        nonexistent_id = 999999
        delete_response = requests.delete(f'{BASE_URL}courier/{nonexistent_id}')
        assert delete_response.status_code == 404, "Должен вернуться код 404 при удалении несуществующего курьера"
        assert delete_response.json().get("message") == "Курьера с таким id нет.", \
            "Сообщение об ошибке должно быть корректным"

    @allure.title("Неуспешный запрос (например, повторное удаление того же курьера)")
    def test_delete_courier_unsuccessful(self, login_courier):
        courier_id = login_courier

        delete_response = requests.delete(f'{BASE_URL}courier/{courier_id}')
        assert delete_response.status_code == 200, "Первый запрос на удаление должен вернуться с кодом 200"

        second_delete_response = requests.delete(f'{BASE_URL}courier/{courier_id}')
        assert second_delete_response.status_code == 404, "Должен вернуться код 404 при повторном удалении курьера"
        assert second_delete_response.json().get("message") == "Курьера с таким id нет.", \
            "Сообщение об ошибке должно быть корректным"
