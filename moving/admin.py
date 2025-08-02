from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ElevatorOption,
    LocationType,
    ParkingType,
    ItemCategory,
    MovingItemOption,
    MovingRequest,
    MovingItem,
)


@admin.register(ElevatorOption)
class ElevatorOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(ParkingType)
class ParkingTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon_preview']
    search_fields = ['name']

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:contain;" />', obj.icon.url)
        return '-'
    icon_preview.short_description = 'Icon'


@admin.register(MovingItemOption)
class MovingItemOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_filter = ['category']
    search_fields = ['name']


class MovingItemInline(admin.TabularInline):
    model = MovingItem
    extra = 0


@admin.register(MovingRequest)
class MovingRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'select_date', 'select_time', 'created_at']
    list_filter = ['select_date']
    search_fields = ['user__username', 'starting_address', 'destination_address']
    inlines = [MovingItemInline]


@admin.register(MovingItem)
class MovingItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'request', 'item_option', 'quantity']
    list_filter = ['item_option__category']
    search_fields = ['item_option__name']
