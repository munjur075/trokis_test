from django.contrib import admin
from .models import HelpersService, HelpCategory


@admin.register(HelpCategory)
class HelpCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(HelpersService)
class HelpersServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'location', 'date', 'time', 'help_category',
        'number_of_helpers', 'offer_per_helper', 'payment_method', 'created_at'
    )
    list_filter = ('help_category', 'payment_method', 'created_at')
    search_fields = ('location', 'user__username', 'user__mobile_number')
    ordering = ('-created_at',)
