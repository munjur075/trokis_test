from django.contrib import admin
from .models import Payment, PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'method', 'status', 'amount', 'service_type', 'service_id', 'created_at')
    list_filter = ('status', 'method__name', 'service_type', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'user__mobile_number')
    ordering = ('-created_at',)
