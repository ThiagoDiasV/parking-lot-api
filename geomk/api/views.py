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


def search_registers_by_id(pk: str) -> Response:
    """
    Try to search an id = pk sent by request.
    """
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(
            {"message": "There isn't an instance with this id at database"},
            status=status.HTTP_404_NOT_FOUND
        )
    serialized_car = CarSerializer(car)
    return Response(serialized_car.data)


def search_cars_by_plate(pk: str) -> Response:
    """
    Try to search cars by plate number.
    """
    cars = Car.objects.filter(plate=pk)
    if not cars:
        return Response(
            {"message": "There aren't registers for this plate"},
            status=status.HTTP_404_NOT_FOUND
        )
    for car in cars:
        if not car.left:
            calculate_time_spent_of_cars(car)
    serialized_cars = [CarSerializer(car).data for car in cars]
    serialized_cars_without_left_time_data = [
        {k: v for k, v in car.items() if k != "left_time"}
        for car in serialized_cars
    ]
    return Response(serialized_cars_without_left_time_data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def retrieve(self, request: Request, pk: str) -> Response:
        """
        Retrieve function overrided to allow retrieving data by id
        and by plate number. Here it's a pk checker. If pk is a digit,
        then this function will try to retrieve the corresponding register.
        If not, it will try to match the sent pk with a plate mask.
        With a match, this plate number will be searched in database.
        Queries by id can only return a single register. Queries by plate
        number can return all registers with the correspondig plate number.
        """
        if pk.isdigit():
            response = search_registers_by_id(pk)
            return response
        else:
            try:
                validate_plate(pk)
            except ValidationError:
                return Response(
                    {"message": "Invalid plate format. Correct format: AAA-1111"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response = search_cars_by_plate(pk)
            return response

    def destroy(self, request: Request, pk: str) -> Response:
        """
        Destroy function overrided to allow destroy registers by
        id and cars by plate number. Deleting one single id, cars that
        have more than one register continue to exist. Deleting all records
        by plate will delete corresponding car from records. 
        """
        if pk.isdigit():
            try:
                entry_register = Car.objects.get(pk=pk)
            except Car.DoesNotExist:
                return Response(
                    {"message": "There isn't an instance with this id at database"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if entry_register:
                entry_register.delete()
                return Response(
                    {"message": "This entry register was succesfully deleted from records"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"message": "There isn't a register with this id at database"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            try:
                validate_plate(pk)
            except ValidationError:
                return Response(
                    {"message": "This isn't a valid plate format"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            car = Car.objects.filter(plate=pk)
            if car:
                car.delete()
                return Response(
                    {"message": "This car was succesfully deleted from records"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"message": "There isn't a car matching this query."},
                    status=status.HTTP_404_NOT_FOUND
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
