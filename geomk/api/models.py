from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
import re


def get_entry_datetime() -> str:
    """
    Get the entry datetime when the car arrives to parking lot.
    """
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def validate_plate(plate: str) -> bool:
    """
    Validate the car's plate.
    """
    regexp = r"^[A-Z]{3}-\d{4}$"
    if not re.search(regexp, plate):
        raise ValidationError(f"{plate} isn't with a valid plate format")


class Car(models.Model):

    entry = models.DateTimeField(default=get_entry_datetime())
    time = models.DurationField()
    paid = models.BooleanField()
    left = models.BooleanField()
    plate = models.CharField(max_length=8, validators=[validate_plate])
