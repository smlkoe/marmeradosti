# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Админ-панель для кастомного пользователя"""
    list_display = ('username', 'email', 'full_name', 'organization_name', 'user_type', 'is_verified', 'is_active')
    list_filter = ('user_type', 'is_verified', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'full_name', 'organization_name', 'inn')
    
    fieldsets = UserAdmin.fieldsets + (
        ('B2B Информация', {
            'fields': (
                'full_name', 'user_type', 'organization_name', 
                'inn', 'phone_number', 'position', 'is_verified'
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('B2B Информация', {
            'fields': (
                'full_name', 'user_type', 'organization_name', 
                'inn', 'phone_number', 'position'
            )
        }),
    )