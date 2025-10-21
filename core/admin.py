from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Product, Cart, CartItem, CustomUser  # ← ДОБАВЬТЕ Cart, CartItem

# СТАРЫЕ МОДЕЛИ (должны быть)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')

# НОВЫЕ МОДЕЛИ КОРЗИНЫ - ДОБАВЬТЕ ЭТОТ КОД
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_active', 'total_quantity', 'total_price')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('product__name', 'cart__user__username')



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