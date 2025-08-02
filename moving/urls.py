from django.urls import path
from .views import (
    CategoriesListView, LocationTypeListView, ParkingTypeListView, ElevatorOptionListView
)

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories-list'),
    path('location-types/', LocationTypeListView.as_view(), name='location-types-list'),
    path('parking-types/', ParkingTypeListView.as_view(), name='parking-types-list'),
    path('elevator-options/', ElevatorOptionListView.as_view(), name='elevator-options-list'),
    

]
