from .base_testcase import BaseTestCase
from string import ascii_uppercase
import re


class TestModels(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_plates_without_4_digits_after_dash_shouldnt_pass(self,):
        sample_with_only_the_digits = self.wrong_plate_1.split("-")[1]
        total_of_digits_of_sample_plate = len(
            [number for number in sample_with_only_the_digits if number.isdigit()]
        )
        self.assertNotEqual(
            total_of_digits_of_sample_plate, self.correct_plate_quantity_of_digits,
        )

    def test_plates_without_3_chars_before_dash_shouldnt_pass(self):
        sample_with_only_the_chars = self.wrong_plate_2.split("-")[0]
        total_of_chars_of_sample_plate = len(
            [char for char in sample_with_only_the_chars if char.isalpha()]
        )
        self.assertNotEqual(
            total_of_chars_of_sample_plate, self.correct_plate_quantity_of_chars,
        )

    def test_plates_with_data_that_isnt_A_to_Z_chars_before_dash_shouldnt_pass(self,):
        sample_with_data_before_dash = self.wrong_plate_3.split("-")[0]
        total_of_no_a_to_z_chars_of_sample_plate = len(
            [
                nochar
                for nochar in sample_with_data_before_dash
                if nochar not in ascii_uppercase
            ]
        )
        self.assertNotEqual(
            total_of_no_a_to_z_chars_of_sample_plate,
            self.correct_plate_quantity_of_no_chars_before_dash,
        )

    def test_plates_with_data_that_isnt_digits_after_dash_shouldnt_pass(self):
        sample_with_data_after_dash = self.wrong_plate_4.split("-")[1]
        total_of_no_digits_of_sample_plate = len(
            [
                nodigit
                for nodigit in sample_with_data_after_dash
                if not nodigit.isdigit()
            ]
        )
        self.assertNotEqual(
            total_of_no_digits_of_sample_plate,
            self.correct_plate_quantity_of_no_digits_after_dash,
        )

    def test_entire_plate_mask(self):
        regexp = r"^[A-Z]{3}-\d{4}$"
        self.assertRegex(self.correct_plate_instance, regexp)
