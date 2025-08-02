from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LineWaitingService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='line_waiting_services')

    # Location
    location = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)

    # Scheduling
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()

    # Job details
    description = models.TextField(help_text="Describe in detail what you need.")

    # Optional offer
    offer_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional offer amount in USD"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Line Waiting Service #{self.id} by {self.user}"