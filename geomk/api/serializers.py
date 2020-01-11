from .models import Car
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "entry_time", "left_time", "time", "paid", "left", "plate"]
        read_only_fields = ["entry_time", "left_time", "time", "paid", "left"]

    def create(self, validated_data: dict) -> Car:
        """
        Overriding create function to avoid POST with cars that already
        are at parking lot and don't left yet.
        """
        car = Car.objects.filter(plate=validated_data.get("plate"))
        if car:
            if not car[0].left:
                raise serializers.ValidationError(
                    "This car is already at parking lot and don't left yet."
                )
        return Car.objects.create(**validated_data)

    # def update(self, instance: Car, validated_data: dict):
    #     """
    #     Overriding update function to
    #     """

    # def update(self, instance, validated_data):
    #     from ipdb import set_trace
    # Consertar a lógica aqui
    # set_trace()

    # if validated_data.get("left"):
    #     if not instance.paid:
    #         raise serializers.ValidationError(
    #             "This car can't left parking lot without paying the ticket."
    #         )
    #     else:
    #         instance.left_time = now()
    #         instance.time = instance.left_time - instance.entry_time
    # instance.paid = validated_data.get("paid", instance.paid)
    # instance.left = validated_data.get("left", instance.left)
    # instance.save()
    # return instance
