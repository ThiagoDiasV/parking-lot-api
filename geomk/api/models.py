from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


# def get_entry_datetime() -> str:
#     """
#     Get the entry datetime when the car arrives to parking lot.
#     """
#     return now()


def validate_plate(plate: str) -> bool:
    """
    Validate the car's plate.
    """
    regexp = r"^[A-Z]{3}-\d{4}$"
    if not re.search(regexp, plate):
        raise ValidationError(f"{plate} isn't a valid plate format")


class Car(models.Model):

    entry_time = models.DateTimeField(default=timezone.now)
    left_time = models.DateTimeField(default="2020-01-01T00:00:00.00")
    time = models.DurationField(default=timedelta(minutes=0))
    paid = models.BooleanField(default=False)
    left = models.BooleanField(default=False)
    plate = models.CharField(max_length=8, validators=[validate_plate])

    def __str__(self):
        return self.plate