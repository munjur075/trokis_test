from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g. "Cash", "bKash"
    code = models.CharField(max_length=50, unique=True)  # e.g. "cash", "bkash"
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    service_type = models.CharField(max_length=50)  # e.g. "errand", "moving"
    service_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.user} - {self.method} - {self.status}"
