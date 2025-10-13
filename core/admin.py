from django.contrib import admin
from .models import Category, Product, Cart, CartItem  # ← ДОБАВЬТЕ Cart, CartItem

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