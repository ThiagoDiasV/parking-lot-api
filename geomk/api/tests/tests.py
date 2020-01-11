from .base_testcase import BaseTestCase
from ..models import validate_plate
from django.core.exceptions import ValidationError


class TestModels(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_if_a_correct_plate_instance_will_pass(self):
        self.assertRegex(
            self.correct_plate_instance, self.plate_correct_regex
        )

    def test_if_plate_with_5_digits_will_pass(self):
        self.assertNotRegex(
            self.wrong_plate_1, self.plate_correct_regex
        )

    def test_if_plate_with_4_chars_will_pass(self):
        self.assertNotRegex(
            self.wrong_plate_2, self.plate_correct_regex
        )

    def test_if_plate_with_digits_before_dash_will_pass(self):
        self.assertNotRegex(
            self.wrong_plate_3, self.plate_correct_regex
        )

    def test_if_plate_with_chars_after_dash_will_pass(self):
        self.assertNotRegex(
            self.wrong_plate_4, self.plate_correct_regex
        )

    def test_if_plate_without_dash_will_pass(self):
        self.assertNotRegex(
            self.wrong_plate_5, self.plate_correct_regex
        )

    def test_if_a_car_with_wrong_plate_will_raise_validation_error(self):
        self.assertRaises(
            ValidationError, validate_plate, self.car_with_wrong_plate_1.plate
        )

    