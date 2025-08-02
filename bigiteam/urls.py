from django.urls import path
from .views import (
    BigItemServiceListView
)

urlpatterns = [
    path('big-item-request/', BigItemServiceListView.as_view(), name='big-item-request-list'),
]
