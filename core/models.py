from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings

class CustomUser(AbstractUser):
    """Расширенная модель пользователя для B2B"""
    
    # Добавляем related_name чтобы избежать конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )
    
    USER_TYPE_CHOICES = (
        ('individual', 'Физическое лицо'),
        ('ip', 'Индивидуальный предприниматель (ИП)'),
        ('company', 'Юридическое лицо (ООО)'),
    )
    
    # Основная информация
    full_name = models.CharField(
        max_length=255, 
        verbose_name="ФИО контактного лица",
        blank=True
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='individual',
        verbose_name="Тип пользователя"
    )
    
    # Информация об организации
    organization_name = models.CharField(
        max_length=255, 
        verbose_name="Наименование организации/ИП",
        blank=True
    )
    
    inn = models.CharField(
        max_length=12,
        verbose_name="ИНН",
        blank=True,
        validators=[RegexValidator(regex=r'^[0-9]{10,12}$', message='ИНН должен содержать 10 или 12 цифр')]
    )
    
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True,
        validators=[RegexValidator(regex=r'^\+?[1-9]\d{7,14}$', message='Введите корректный номер телефона')]
    )
    
    # Дополнительная информация
    position = models.CharField(
        max_length=100,
        verbose_name="Должность",
        blank=True
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Подтвержденный аккаунт"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )
    
    def __str__(self):
        return f"{self.username} - {self.organization_name or self.full_name}"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название мармелада")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория"
    )
    description = models.TextField(verbose_name="Описание продукта")
    weight = models.PositiveIntegerField(help_text="Указывается в граммах", verbose_name="Вес упаковки")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Оптовая цена (за упаковку)")
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активный (доступен для заказа)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

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