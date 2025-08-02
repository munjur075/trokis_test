from django.db import models
from django.contrib.auth import get_user_model
from payments.models import PaymentMethod  # dynamic payment methods

User = get_user_model()

class ScheduleType(models.TextChoices):
    NOW = 'now', 'Right Now'
    LATER = 'later', 'For Later'

class ErrandService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='errand_services')
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='errand_services'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ErrandService #{self.id} by {self.user}"

class ErrandItem(models.Model):
    service = models.ForeignKey(ErrandService, on_delete=models.CASCADE, related_name='errand_items')
    
    description = models.TextField()
    provider_selects_location = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)

    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    
    schedule_type = models.CharField(max_length=10, choices=ScheduleType.choices)
    scheduled_date = models.DateField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Errand for {self.contact_name} (Service ID: {self.service_id})"
