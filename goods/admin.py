# goods/admin.py
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count')
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Количество товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description', 'composition')