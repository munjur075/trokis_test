
# starting location page 
starting_address 
address_line_2 (Apt, Suite, etc.)
select_date 
select_time 

location_type:
   house
   appartment
   office/retail space
   supermarket chain/ mall
   farm house
   other

floor_level example: 1,2,3,4,5,6,7,8,9,10

is_there_elevator:
    Freight elevator
    Normal elevator
    No elevator
    first floor
    Farm house
    Stairs are wide
    Stairs are narrow

# click next to continue
#Desination location page
destination_address
destination_address_line_2 (Apt, Suite, etc.)
location_type:
   house
   appartment
   office/retail space
   supermarket chain/ mall
   farm house
   other

floor_level example: 1,2,3,4,5,6,7,8,9,10

is_there_elevator:
    Freight elevator
    Normal elevator
    No elevator
    first floor
    Farm house
    Stairs are wide
    Stairs are narrow

# click next to continue
# Moving Items selection page
bedroom:
    king bed : 2
    queen bed : 2
    twin bed : 2
    bunk bed : 2
master_bedroom:
    king bed : 1
    queen bed : 1
    twin bed : 1
living_room:
    sofa : 1
    loveseat : 1
kitchen:
    dining table : 1
    chairs : 4
    refrigerator : 1
bathroom:
    toilet : 1
    shower : 1
    bathtub : 1


# click next to continue
# Moving Items review page
# Display all the information entered by the user
# get quotes to finalize the finding Movers page
# Display the list of movers with their quotes
# User can select a mover and confirm the booking


# ------------------------------------------
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# ✅ Dynamic Elevator Options
class ElevatorOption(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Dynamic Location Types
class LocationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ParkingType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Location Model (for both start and destination)
class Location(models.Model):
    address = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    location_type = models.ForeignKey(LocationType, on_delete=models.SET_NULL, null=True)
    floor_level = models.PositiveIntegerField()
    elevator = models.ForeignKey(ElevatorOption, on_delete=models.SET_NULL, null=True)
    parking_type = models.CharField(max_length=100, blank=True, null=True)  # e.g., Street, Garage, Lot

    def __str__(self):
        return f"{self.address} - {self.location_type.name}"


# ✅ Main Moving Request
class MovingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_location = models.OneToOneField(Location, related_name='start_location', on_delete=models.CASCADE)
    destination_location = models.OneToOneField(Location, related_name='end_location', on_delete=models.CASCADE)
    select_date = models.DateField()
    select_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Move by {self.user} on {self.select_date}"


# ✅ Item Category (e.g., Bedroom, Kitchen)
class ItemCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Available Item Options (e.g., King Bed, Sofa)
class MovingItemOption(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# ✅ Items User Selected for Moving
class MovingItem(models.Model):
    request = models.ForeignKey(MovingRequest, on_delete=models.CASCADE, related_name='items')
    item_option = models.ForeignKey(MovingItemOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item_option.name} x{self.quantity}"


# ✅ Quotes from Movers
class MoverQuote(models.Model):
    moving_request = models.ForeignKey(MovingRequest, on_delete=models.CASCADE, related_name='quotes')
    mover_name = models.CharField(max_length=100)
    quote_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_time_hours = models.DecimalField(max_digits=5, decimal_places=2)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.mover_name} - ${self.quote_amount}"


# ✅ Final Booking Confirmation
class ConfirmedBooking(models.Model):
    moving_request = models.OneToOneField(MovingRequest, on_delete=models.CASCADE, related_name='confirmed_booking')
    selected_quote = models.OneToOneField(MoverQuote, on_delete=models.CASCADE)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking confirmed with {self.selected_quote.mover_name}"
