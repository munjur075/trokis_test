from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'mobile_number', 'id', 'full_name', 'email', 'role',
        'is_active', 'is_staff', 'is_superuser', 'is_verified'
    )
    search_fields = ('mobile_number', 'full_name', 'email')
