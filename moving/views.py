from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from .models import ItemCategory, MovingItemOption, ElevatorOption, LocationType, ParkingType

class CategoriesListView(APIView):
    def get(self, request):
        categories = ItemCategory.objects.all().reverse()

        if not categories:
            return Response({'message': 'No item categories found.'}, status=status.HTTP_404_NOT_FOUND)
        # print("item categories:",categories)
       
        category_data = []
        for category in categories:
            items = MovingItemOption.objects.filter(category=category)
            # print('item list',items)

            item_data = [{'id': item.id, 'name': item.name} for item in items]
            category_data.append({
                'id': category.id,
                'name': category.name,
                'icon': category.icon.url if category.icon else '',
                'items': item_data
            })

        return Response (category_data, status=status.HTTP_200_OK)

class LocationTypeListView(APIView):
    def get(self, request):
        location_types = LocationType.objects.all()

        if not location_types:
            return Response({'message': 'No location types found.'}, status=status.HTTP_404_NOT_FOUND)
        
        location_type_data = [{'id': loc.id, 'name': loc.name} for loc in location_types]

        return Response(location_type_data, status=status.HTTP_200_OK)

class ParkingTypeListView(APIView):
    def get(self, request):
        parking_types = ParkingType.objects.all()
        if not parking_types:
            return Response({'message': 'No parking types found.'}, status=status.HTTP_404_NOT_FOUND)
        parking_type_data = [{'id': park.id, 'name': park.name} for park in parking_types]

        return Response(parking_type_data, status=status.HTTP_200_OK)

class ElevatorOptionListView(APIView):
    def get(self, request):
        elevator_options = ElevatorOption.objects.all()
        if not elevator_options:
            return Response({'message': 'No elevator options found.'}, status=status.HTTP_404_NOT_FOUND)
        
        elevator_option_data = [{'id': elev.id, 'name': elev.name} for elev in elevator_options]

        return Response(elevator_option_data, status=status.HTTP_200_OK)
    