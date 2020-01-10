from django.db import models
from datetime import datetime


class Car(models.Model):

    def get_entry_datetime(self) -> str:
        """
        Get the entry datetime when the car arrives to parking lot.
        """
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def validate_plate(self, plate: str) -> bool:
        """
        Validate the car's plate.
        """
        pass

    entry = models.DateTimeField(default=get_entry_datetime())
    time = models.DurationField()
    paid = models.BooleanField()
    left = models.BooleanField()
    plate = models.CharField(max_length=8, validators=[validate_plate])
