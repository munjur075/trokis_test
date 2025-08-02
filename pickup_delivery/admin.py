from django.contrib import admin
from .models import PickupDeliveryService, DeliveryStop

# Use StackedInline for vertically displaying delivery stop fields
# (Use TabularInline instead if you prefer compact, row-style form layout)
class DeliveryStopInline(admin.StackedInline):
    model = DeliveryStop
    extra = 0  # Show zero blank forms by default (change to 1+ if needed)
    fields = (
        'delivery_location',
        'delivery_address_line_2',
        'delivery_name',
        'delivery_phone_number',
        'delivery_description',
        'stop_order',
    )
    ordering = ('stop_order',)

# Admin panel configuration for PickupDeliveryService
@admin.register(PickupDeliveryService)
class PickupDeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle_type', 'payment_method', 'created_at')
    list_filter = ('vehicle_type', 'payment_method', 'created_at')
    search_fields = ('user__username', 'pickup_location', 'pickup_phone_number')
    inlines = [DeliveryStopInline]


# Optional: You can uncomment this if you want a separate admin panel for DeliveryStop

# @admin.register(DeliveryStop)
# class DeliveryStopAdmin(admin.ModelAdmin):
#     list_display = ('id', 'service', 'delivery_location', 'delivery_name', 'delivery_phone_number')
#     search_fields = ('delivery_location', 'delivery_name', 'delivery_phone_number')
