from django.db import models
from django.conf import settings
from goods.models import Product

# МОДЕЛИ КОРЗИНЫ
class Cart(models.Model):
    """Модель корзины пользователя"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return f"Корзина {self.user.username}"

    def total_quantity(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price() for item in self.items.all())

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

class CartItem(models.Model):
    """Элемент корзины - конкретный товар"""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        """Стоимость позиции (цена × количество)"""
        return self.quantity * self.product.price

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
        unique_together = ['cart', 'product']