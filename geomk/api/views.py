from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Car, validate_plate
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.timezone import now
from django.core.exceptions import ValidationError


def calculate_time_spent_of_cars(car: Car) -> None:
    """
    Calculate the time spent of a car at parking lot when the info
    by plate is retrieved.
    """
    car.left_time = now()
    duration_in_seconds = (car.left_time - car.entry_time).seconds
    duration_in_minutes = round(duration_in_seconds / 60)
    car.time = f"{duration_in_minutes} minutes"
    car.save()


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def retrieve(self, request: Request, pk: str) -> Response:
        try: 
            validate_plate(pk)
        except ValidationError:
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
        cars = Car.objects.filter(plate=pk)
        for car in cars:
            if not car.left:
                calculate_time_spent_of_cars(car)
        serialized_cars = [CarSerializer(car).data for car in cars]
        serialized_cars_to_response = [
            {k: v for k, v in car.items() if k != "left_time"}
            for car in serialized_cars
        ]
        return Response(serialized_cars_to_response)

    def destroy(self, request: Request, pk: str) -> Response:
        car = Car.objects.filter(plate=pk)
        car.delete()
        return Response(
            {"message": "This car was succesfully deleted from records"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["get", "put"])
    def pay(self, request: Request, pk: str) -> Response:
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
    def out(self, request: Request, pk: str) -> Response:
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
            calculate_time_spent_of_cars(car)
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
