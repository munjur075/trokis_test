from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


# ✅ Elevator Options (Dynamic)
class ElevatorOption(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ Location Types (Dynamic)
class LocationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ Parking Types (Dynamic)
class ParkingType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ Item Category (e.g., Bedroom, Kitchen)
class ItemCategory(models.Model):
    icon = models.ImageField(upload_to='item_category_icons/', blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Item Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ✅ Item Options (e.g., King Bed, Sofa)
class MovingItemOption(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['category__name', 'name']
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# ✅ Main Moving Request
class MovingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moving_requests')

    # Starting location
    starting_address = models.CharField(max_length=255)
    starting_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    select_date = models.DateField()
    select_time = models.TimeField()
    starting_location_type = models.ForeignKey(LocationType, on_delete=models.SET_NULL, null=True, related_name='start_requests')
    starting_floor_level = models.PositiveIntegerField()
    starting_elevator = models.ForeignKey(ElevatorOption, on_delete=models.SET_NULL, null=True, related_name='start_requests')
    starting_parking_type = models.ForeignKey(ParkingType, on_delete=models.SET_NULL, null=True, related_name='start_requests')

    # Destination location
    destination_address = models.CharField(max_length=255)
    destination_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    destination_location_type = models.ForeignKey(LocationType, on_delete=models.SET_NULL, null=True, related_name='destination_requests')
    destination_floor_level = models.PositiveIntegerField()
    destination_elevator = models.ForeignKey(ElevatorOption, on_delete=models.SET_NULL, null=True, related_name='destination_requests')
    destination_parking_type = models.ForeignKey(ParkingType, on_delete=models.SET_NULL, null=True, related_name='destination_requests')

    upload_media = models.FileField(
        upload_to='moving_uploads/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi', 'mkv'])]
    )
    additional_notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Move by {self.user} on {self.select_date}"



# ✅ Items Selected by User in a Moving Request
class MovingItem(models.Model):
    request = models.ForeignKey(MovingRequest, on_delete=models.CASCADE, related_name='selected_items')
    item_option = models.ForeignKey(MovingItemOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item_option.name} x{self.quantity}"
