from rest_framework.test import APITestCase
from .base_testcase import BaseTestCase
from ..serializers import CarSerializer


class BaseAPITestCase(APITestCase, BaseTestCase):
    def setUp(self):
        super().setUp()
        self.main_url = "/parking/"
        self.correct_car_json_repr = CarSerializer(
            self.car_with_correct_plate_1
        )
        self.car_already_at_parking_lot_json_repr = CarSerializer(
            self.car_already_at_parking_lot
        )
        self.leaving_car_json_repr = CarSerializer(self.returned_car)
        self.wrong_car_json_repr = CarSerializer(self.car_with_wrong_plate_1)
