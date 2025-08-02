from django.contrib import admin
from .models import ErrandService, ErrandItem


# Inline display of each errand item within the service
class ErrandItemInline(admin.StackedInline):
    model = ErrandItem
    extra = 0
    fields = (
        'description',
        'provider_selects_location',
        'location',
        'address_line_2',
        'contact_name',
        'contact_phone',
        'schedule_type', 
        'scheduled_date', 
        'scheduled_time',
    )


@admin.register(ErrandService)
class ErrandServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('user__username', 'user__mobile_number')  # adjust based on your user model
    inlines = [ErrandItemInline]
    ordering = ('-created_at',)


# @admin.register(ErrandItem)
# class ErrandItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'service', 'description', 'contact_name', 'provider_selects_location')
#     search_fields = ('description', 'contact_name', 'contact_phone', 'location')
#     list_filter = ('provider_selects_location',)
