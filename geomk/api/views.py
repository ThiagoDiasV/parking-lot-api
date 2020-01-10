from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_fields = ["left_time", "time", "paid", "left", "plate"]

    # @action(detail=True, methods=['put'])
    # def out(self, request, pk)
