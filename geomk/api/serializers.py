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
        If the same car came again to parking lot, the previous register
        will be deleted.
        """
        car = Car.objects.filter(plate=validated_data.get("plate"))[0]
        if car:
            if not car.left:
                raise serializers.ValidationError(
                    "This car is already at parking lot and don't left yet."
                )
            elif car.left:
                car.delete()
        return Car.objects.create(**validated_data)
