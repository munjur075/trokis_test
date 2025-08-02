from django.contrib import admin
from .models import LineWaitingService

@admin.register(LineWaitingService)
class LineWaitingServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'location',
        'scheduled_date',
        'scheduled_time',
        'offer_amount',
        'created_at',
    )
    list_filter = ('scheduled_date',)
    search_fields = ('user__username', 'location', 'description')
    ordering = ('-created_at',)
