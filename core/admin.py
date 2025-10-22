from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Category, Product, Cart, CartItem, CustomUser
from django.contrib.auth.admin import UserAdmin

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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'product_count')
    actions = ['delete_selected_categories']
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Количество товаров'
    
    def delete_selected_categories(self, request, queryset):
        """Кастомное действие для удаления категорий"""
        for category in queryset:
            # Проверяем есть ли товары в этой категории
            if category.product_set.exists():
                # Переносим товары в категорию "Без категории" или устанавливаем NULL
                uncategorized, created = Category.objects.get_or_create(
                    name='Без категории',
                    defaults={'description': 'Товары без категории'}
                )
                Product.objects.filter(category=category).update(category=uncategorized)
            
            # Удаляем категорию
            category.delete()
        
        self.message_user(request, f"Успешно удалено {queryset.count()} категорий", messages.SUCCESS)
        return HttpResponseRedirect(request.get_full_path())
    
    delete_selected_categories.short_description = "Удалить выбранные категории (с обработкой товаров)"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    actions = ['delete_selected_products']
    
    def delete_selected_products(self, request, queryset):
        """Кастомное действие для удаления товаров"""
        for product in queryset:
            # Сначала удаляем все связанные элементы корзины
            CartItem.objects.filter(product=product).delete()
            # Затем удаляем сам товар
            product.delete()
        
        self.message_user(request, f"Успешно удалено {queryset.count()} товаров", messages.SUCCESS)
        return HttpResponseRedirect(request.get_full_path())
    
    delete_selected_products.short_description = "Удалить выбранные товары (с обработкой корзины)"

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