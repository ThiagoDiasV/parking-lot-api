from .models import Car
from rest_framework import serializers
from django.utils.timezone import now


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "entry_time", "left_time", "time", "paid", "left", "plate"]
        read_only_fields = ["entry_time", "left_time", "time", "paid", "left"]

    def create(self, validated_data):
        car = Car.objects.filter(plate=validated_data.get("plate"))
        if car:
            if not car[0].left:
                # from ipdb import set_trace; set_trace()
                raise serializers.ValidationError(
                    "This car is already at parking lot and don't left yet."
                )
        return Car.objects.create(**validated_data)

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
