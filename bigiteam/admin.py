from django.contrib import admin
from .models import BigItemService, BigItemStop

class BigItemStopInline(admin.TabularInline):
    model = BigItemStop
    extra = 0

@admin.register(BigItemService)
class BigItemServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'pickup_location', 'pickup_address_line_2', 'dropoff_location', 'dropoff_address_line_2', 'service_time']
    inlines = [BigItemStopInline]