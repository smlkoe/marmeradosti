from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
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