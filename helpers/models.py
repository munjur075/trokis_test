from django.db import models
from django.contrib.auth import get_user_model
from payments.models import PaymentMethod  # if you're using dynamic payment methods

User = get_user_model()

# Optional (but better): dynamic types of help
class HelpCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class HelpersService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helpers_services')
    
    # Location info
    location = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)

    # Date & time
    date = models.DateField()
    time = models.TimeField()

    # Help category (e.g., moving, cleaning, etc.)
    help_category = models.ForeignKey(HelpCategory, on_delete=models.SET_NULL, null=True)

    # Core fields
    number_of_helpers = models.PositiveIntegerField()
    estimated_duration_hours = models.DecimalField(max_digits=5, decimal_places=2, help_text="Estimated duration in hours")
    offer_per_helper = models.DecimalField(max_digits=10, decimal_places=2)
    additional_details = models.TextField(blank=True, null=True)

    # Payment method (linked to dynamic method model)
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='helpers_services'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HelpersService #{self.id} by {self.user}"
