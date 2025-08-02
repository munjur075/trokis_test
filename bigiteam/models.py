from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BigItemService(models.Model):
    SERVICE_TIME_CHOICES = [
        ('now', 'Now'),
        ('later', 'Schedule for Later'),
    ]

    LOADING_HELP_CHOICES = [
        ('self', 'I will load and unload the cargo myself'),
        ('need_help', "I want help loading and unloading the cargo"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile_banking', 'Mobile Banking'),
        # Add more methods as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='big_item_requests')
    pickup_location = models.CharField(max_length=255)
    pickup_address_line_2 = models.CharField(max_length=255, blank=True, null=True)

    dropoff_location = models.CharField(max_length=255)
    dropoff_address_line_2 = models.CharField(max_length=255, blank=True, null=True)

    service_time = models.CharField(max_length=10, choices=SERVICE_TIME_CHOICES)
    scheduled_time = models.DateTimeField(blank=True, null=True)

    loading_help = models.CharField(max_length=15, choices=LOADING_HELP_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BigItemService - {self.user} - {self.pickup_location} to {self.dropoff_location}"


class BigItemStop(models.Model):
    service = models.ForeignKey(BigItemService, on_delete=models.CASCADE, related_name='stops')
    stop_location = models.CharField(max_length=255)
    stop_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(help_text="Order of the stop", default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Stop at {self.stop_location} for Service ID {self.service.id}"

