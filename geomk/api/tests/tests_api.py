from rest_framework import status
from .base_apitestcase import BaseAPITestCase
from .base_testcase import BaseTestCase


class CarApiTests(BaseAPITestCase, BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_if_main_url_will_list_parking_lot_existing_cars(self):
        response_200_OK = self.client.get(self.main_url)
        self.assertEqual(response_200_OK.status_code, status.HTTP_200_OK)

    def test_if_a_correct_car_instance_can_be_created(self):
        response_201_CREATED = self.client.post(
            self.main_url, self.correct_car_json_repr.data, format="json"
        )
        self.assertEqual(
            response_201_CREATED.status_code, status.HTTP_201_CREATED
        )

    def test_if_a_car_that_doesnt_left_yet_can_enter_again(self):
        response_400_BR = self.client.post(
            self.main_url,
            self.car_already_at_parking_lot_json_repr.data,
            format="json",
        )
        self.assertEqual(
            response_400_BR.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_if_a_wrong_car_instance_with_wrong_plate_can_be_created(self):
        response_400_BR = self.client.post(
            self.main_url, self.wrong_car_json_repr.data, format="json"
        )
        self.assertEqual(
            response_400_BR.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_if_it_is_possible_to_get_car_history_by_plate_instead_by_id(self):
        response_200_OK = self.client.get(
            f"{self.main_url}{self.car_1_at_database.plate}/", format="json"
        )
        self.assertEqual(response_200_OK.status_code, status.HTTP_200_OK)

    def test_if_it_is_possible_to_get_entry_register_by_id(self):
        response_200_OK = self.client.get(f"{self.main_url}3/", format="json")
        self.assertEqual(response_200_OK.status_code, status.HTTP_200_OK)

    def test_if_unexisting_id_will_return_http_404(self):
        response_404_NOT_FOUND = self.client.get(
            f"{self.main_url}666/", format="json"
        )
        self.assertEqual(
            response_404_NOT_FOUND.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_if_incorrect_plate_format_will_return_http_400(self):
        response_400_BR = self.client.get(
            f"{self.main_url}{self.wrong_plate_1}/", format="json"
        )
        self.assertEqual(
            response_400_BR.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_if_it_is_possible_to_delete_car_by_plate_from_database(self):
        response_204_NO_CONTENT = self.client.delete(
            f"{self.main_url}{self.car_1_at_database.plate}/", format="json"
        )
        self.assertEqual(
            response_204_NO_CONTENT.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_if_it_is_possible_to_delete_register_by_id_from_database(self):
        response_204_NO_CONTENT = self.client.delete(
            f"{self.main_url}{self.car_1_at_database.id}/", format="json"
        )
        self.assertEqual(
            response_204_NO_CONTENT.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_if_it_is_possible_to_delete_unexisting_car_from_database(self):
        response_404_NOT_FOUND = self.client.delete(
            f"{self.main_url}250/", format="json"
        )
        self.assertEqual(
            response_404_NOT_FOUND.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_if_a_car_with_unpaid_ticket_can_leave_parking_lot(self):
        response_401_UNAUTHORIZED = self.client.put(
            f"{self.main_url}{self.car_1_at_database.id}/out/", format="json"
        )
        self.assertEqual(
            response_401_UNAUTHORIZED.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_if_a_car_with_unpaid_ticket_can_pay_the_ticket(self):
        response_200_OK = self.client.put(
            f"{self.main_url}{self.car_1_at_database.id}/pay/", format="json"
        )
        self.assertEqual(response_200_OK.status_code, status.HTTP_200_OK)

    def test_if_a_car_with_paid_ticket_can_leave_parking_lot(self):
        response_200_OK = self.client.put(
            f"{self.main_url}{self.car_2_at_database.id}/out/", format="json"
        )
        self.assertEqual(response_200_OK.status_code, status.HTTP_200_OK)

    def test_if_a_car_that_already_left_can_came_by_again(self):
        response_201_CREATED = self.client.post(
            self.main_url, self.leaving_car_json_repr.data, format="json"
        )
        self.assertEqual(
            response_201_CREATED.status_code, status.HTTP_201_CREATED
        )

    def test_if_it_is_possible_to_pay_ticket_when_pk_is_plate_number(self):
        response_400_BR = self.client.put(
            f"{self.main_url}{self.car_1_at_database.plate}/pay/",
            format="json"
        )
        self.assertEqual(
            response_400_BR.status_code, status.HTTP_400_BAD_REQUEST
        )
