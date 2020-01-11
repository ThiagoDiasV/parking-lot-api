from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Car
from .serializers import CarSerializer
from rest_framework.response import Response
from django.utils.timezone import now


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def retrieve(self, request, pk):
        try:
            car = Car.objects.filter(plate=pk)[0]
        except IndexError:
            return Response(
                {
                    "message": "Instance not found. "
                    "If you are searching for a car by id, "
                    "try to search by plate number. "
                    "Remember to search using uppercase: "
                    "/parking/AAA-1234 instead of "
                    "/parking/aaa-1234."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        car_serialized = CarSerializer(car)
        car_serialized = {
            k: v
            for k, v in car_serialized.data.items()
            if k != "entry_time" and k != "left_time"
        }
        return Response(car_serialized)

    def destroy(self, request, pk):
        car = Car.objects.filter(plate=pk)[0]
        car.delete()
        return Response(
            {"message": "Instance was succesfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["get", "put"])
    def pay(self, request, pk) -> Response:
        car = self.get_object()
        if not car.paid:
            car.paid = True
            car.save()
            return Response(
                {"message": "The ticket was paid succesfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "This car's ticket was already paid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get", "put"])
    def out(self, request, pk) -> Response:
        car = self.get_object()
        if not car.paid:
            return Response(
                {
                    "message": "This car can't leave parking lot before "
                    "paying the ticket"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        elif not car.left:
            car.left = True
            car.left_time = now()
            duration_in_seconds = (car.left_time - car.entry_time).seconds
            duration_in_minutes = round(duration_in_seconds / 60)
            car.time = f"{duration_in_minutes} minutes"
            car.save()
            return Response(
                {
                    "message": "Ok, you can leave. Thanks and we "
                    "expect to see you again."
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": "There isn't a car with this "
                    "specifications at parking lot"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
