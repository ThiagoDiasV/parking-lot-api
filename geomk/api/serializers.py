from .models import Car
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ["entry_time", "left_time", "time", "paid", "left"]

    def create(self, validated_data: dict) -> Car:
        """
        Overriding create function to avoid POST with cars that already
        are at parking lot and don't left yet.
        Cars with plate registered can only enter if they already left the last
        time.
        """
        try:
            cars = Car.objects.filter(plate=validated_data.get("plate"))
            last_register = cars.last()
            if last_register:
                if not last_register.left:
                    raise serializers.ValidationError(
                        "Car already at parking lot and don't left yet."
                    )
        except IndexError:
            pass
        return Car.objects.create(**validated_data)
