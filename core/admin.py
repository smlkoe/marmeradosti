from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') # Что показывать в списке

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'is_active')
    list_filter = ('category', 'is_active') # Фильтр сбоку
    search_fields = ('name', 'description') # Поле поиска