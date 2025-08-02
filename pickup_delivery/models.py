from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Choices
VEHICLE_CHOICES = (
    ('moto', 'Moto'),
    ('car', 'Car'),
)

PAYMENT_METHODS = (
    ('cash', 'Cash'),
    ('online', 'Online'),
    ('card', 'Card'),
)

class PickupDeliveryService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_deliveries')
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES)

    # Pickup Information
    pickup_location = models.CharField(max_length=255)
    pickup_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    pickup_name = models.CharField(max_length=100)
    pickup_phone_number = models.CharField(max_length=20)
    pickup_description = models.TextField(help_text="What do you need to pickup?")

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.vehicle_type} - {self.created_at.strftime('%Y-%m-%d')}"

class DeliveryStop(models.Model):
    service = models.ForeignKey(PickupDeliveryService, on_delete=models.CASCADE, related_name='delivery_stops')
    
    delivery_location = models.CharField(max_length=255)
    delivery_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    delivery_name = models.CharField(max_length=100)
    delivery_phone_number = models.CharField(max_length=20)
    delivery_description = models.TextField(help_text="What do you need to deliver at this location?")

    stop_order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Delivery Stop #{self.stop_order} for Service ID {self.service.id}"
