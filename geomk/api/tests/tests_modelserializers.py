from .base_testcase import BaseTestCase
from ..models import validate_plate
from ..serializers import CarSerializer
from django.core.exceptions import ValidationError


class TestModelsSerializers(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_if_a_correct_plate_instance_will_pass(self):
        self.assertRegex(self.correct_plate_instance, self.plate_correct_regex)

    def test_if_plate_with_5_digits_will_pass(self):
        self.assertNotRegex(self.wrong_plate_1, self.plate_correct_regex)

    def test_if_plate_with_4_chars_will_pass(self):
        self.assertNotRegex(self.wrong_plate_2, self.plate_correct_regex)

    def test_if_plate_with_digits_before_dash_will_pass(self):
        self.assertNotRegex(self.wrong_plate_3, self.plate_correct_regex)

    def test_if_plate_with_chars_after_dash_will_pass(self):
        self.assertNotRegex(self.wrong_plate_4, self.plate_correct_regex)

    def test_if_plate_without_dash_will_pass(self):
        self.assertNotRegex(self.wrong_plate_5, self.plate_correct_regex)

    def test_if_a_car_with_wrong_plate_will_raise_validation_error(self):
        self.assertRaises(
            ValidationError, validate_plate, self.car_with_wrong_plate_1.plate
        )

    def test_if_a_car_that_havent_paid_yet_can_leave_parking_lot(self):
        paid_status = self.car_with_wrong_parameters_paid_and_left.paid
        left_status = self.car_with_wrong_parameters_paid_and_left.left
        if left_status and not paid_status:
            self.assertNotEqual(left_status, paid_status)

    def test_serialized_car_with_wrong_plate_can_enter_parking_lot(self):
        car_serialized = CarSerializer(self.car_with_wrong_plate_1)
        self.assertRaises(ValidationError, validate_plate, car_serialized.data["plate"])
