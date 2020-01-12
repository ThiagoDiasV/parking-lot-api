from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


def validate_plate(plate: str):
    """
    Validate the car's plate.
    """
    regexp = r"^[A-Z]{3}-\d{4}$"
    if not re.search(regexp, plate):
        raise ValidationError(
            f"{plate} isn't a valid plate format. The correct format is AAA-1111"
        )


class Car(models.Model):

    entry_time = models.DateTimeField(default=timezone.now)
    left_time = models.DateTimeField(default="2020-01-01T00:00:00.00")
    time = models.CharField(max_length=13, default="0 minutes")
    paid = models.BooleanField(default=False)
    left = models.BooleanField(default=False)
    plate = models.CharField(max_length=8, validators=[validate_plate])
