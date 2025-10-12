from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание") # blank=True - поле необязательное

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название мармелада")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
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