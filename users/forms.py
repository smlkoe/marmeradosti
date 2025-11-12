# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации для B2B клиентов"""
    
    USER_TYPE_CHOICES = (
        ('individual', 'Физическое лицо'),
        ('ip', 'Индивидуальный предприниматель (ИП)'),
        ('company', 'Юридическое лицо (ООО)'),
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email для связи'
        })
    )
    
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов Иван Иванович'
        })
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    organization_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ООО "Ромашка" или ИП Иванов И.И.'
        })
    )
    
    inn = forms.CharField(
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567890'
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'full_name', 'user_type', 'organization_name', 
            'inn', 'phone_number'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин для входа'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_inn(self):
        inn = self.cleaned_data.get('inn')
        if inn and User.objects.filter(inn=inn).exists():
            raise ValidationError('Пользователь с таким ИНН уже зарегистрирован')
        return inn

class CustomAuthenticationForm(AuthenticationForm):
    """Кастомная форма авторизации"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин или Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""
    class Meta:
        model = User
        fields = ['full_name', 'organization_name', 'inn', 'phone_number', 'position']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }