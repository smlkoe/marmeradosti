from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm
from .models import Product, Category, Cart, CartItem

# Получаем кастомную модель пользователя
User = get_user_model()

def home(request):
    """Главная страница"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """Страница 'О нас'"""
    return render(request, 'core/about.html')

def product_list(request):
    """Страница со списком всех продуктов"""
    products = Product.objects.filter(is_active=True)
    context = {'products': products}
    return render(request, 'core/product_list.html', context)

# ФУНКЦИИ КОРЗИНЫ
def get_cart(request):
    """Получает или создает корзину для текущего пользователя"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, 
            is_active=True
        )
        return cart
    return None

def cart_add(request, product_id):
    """Добавление товара в корзину"""
    if not request.user.is_authenticated:
        messages.info(request, 'Для добавления товаров в корзину необходимо авторизоваться')
        return redirect('core:login')  # ← Редирект на наш login URL
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    if cart:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
        messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    
    return redirect('core:product_list')

def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    if not request.user.is_authenticated:
        messages.info(request, 'Для управления корзиной необходимо авторизоваться')
        return redirect('core:login')  # ← Редирект на наш login URL
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    if cart:
        CartItem.objects.filter(cart=cart, product=product).delete()
        messages.success(request, f'Товар "{product.name}" удален из корзины')
    
    return redirect('core:cart_detail')

def cart_clear(request):
    """Полная очистка корзины"""
    if not request.user.is_authenticated:
        messages.info(request, 'Для управления корзиной необходимо авторизоваться')
        return redirect('core:login')  # ← Редирект на наш login URL
    
    cart = get_cart(request)
    if cart:
        cart.items.all().delete()
        messages.success(request, 'Корзина очищена')
    
    return redirect('core:cart_detail')
@login_required
def cart_detail(request):
    """Страница просмотра корзины"""
    # Проверяем авторизацию пользователя
    if not request.user.is_authenticated:
        return render(request, 'core/cart_empty_unauthorized.html')
    
    # Для авторизованных пользователей показываем корзину
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart) if cart else []
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'core/cart_detail.html', context)

@login_required
def cart_clear(request):
    """Полная очистка корзины"""
    cart = get_cart(request)
    if cart:
        cart.items.all().delete()
        messages.success(request, 'Корзина очищена')
    
    return redirect('core:cart_detail')

# ФУНКЦИИ АУТЕНТИФИКАЦИИ
def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('core:profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Автоматический вход после регистрации
            login(request, user)
            
            messages.success(
                request, 
                f'Добро пожаловать, {user.full_name}! Ваш аккаунт успешно создан.'
            )
            return redirect('core:profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/auth/register.html', {'form': form})

def login_view(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('core:profile')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.full_name}!')
                
                # Перенаправляем на страницу, с которой пришел пользователь
                next_url = request.GET.get('next', 'core:profile')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/auth/login.html', {'form': form})

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('core:home')

@login_required
def profile_view(request):
    """Профиль пользователя"""
    user_orders = []  # Здесь позже добавим историю заказов
    
    context = {
        'user': request.user,
        'user_orders': user_orders,
    }
    return render(request, 'core/auth/profile.html', context)

@login_required
def profile_edit_view(request):
    """Редактирование профиля с использованием формы"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('core:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'core/auth/profile_edit.html', {'form': form})

# Контекстный процессор для корзины
def get_user_cart(request):
    """Получает корзину текущего пользователя для контекста"""
    if request.user.is_authenticated:
        try:
            return Cart.objects.get(user=request.user, is_active=True)
        except Cart.DoesNotExist:
            return None
    return None