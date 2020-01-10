from django.test import TestCase


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.wrong_plate_1 = "ABC-12345"
        self.wrong_plate_2 = "ABCD-1234"
        self.wrong_plate_3 = "A1D-1234"
        self.wrong_plate_4 = "ABC-A123"
        self.correct_plate_instance = "AAA-9999"
        self.correct_plate_quantity_of_digits = 4
        self.correct_plate_quantity_of_chars = 3
        self.correct_plate_quantity_of_no_digits_after_dash = 0
        self.correct_plate_quantity_of_no_chars_before_dash = 0
