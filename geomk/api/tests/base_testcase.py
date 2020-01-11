from django.test import TestCase
from ..models import Car


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.wrong_plate_1 = "ABC-12345"
        self.wrong_plate_2 = "ABCD-1234"
        self.wrong_plate_3 = "A1D-1234"
        self.wrong_plate_4 = "ABC-A123"
        self.wrong_plate_5 = "ABC1234"
        self.correct_plate_instance = "AAA-9999"
        self.plate_correct_regex = r"^[A-Z]{3}-\d{4}$"
        self.car_with_wrong_plate_1 = Car(
            id=1,
            entry_time="2020-01-11T09:52:00.111562-03:00",
            left_time="2020-01-01T00:00:00-03:00",
            time="0 minutes",
            paid=False,
            left=False,
            plate="AAA-99999"
        )
        self.car_with_correct_plate_1 = Car(
            id=1,
            entry_time="2020-01-11T09:52:00.111562-03:00",
            left_time="2020-01-01T00:00:00-03:00",
            time="0 minutes",
            paid=False,
            left=False,
            plate="AAA-9999"
        )
