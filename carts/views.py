# carts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from goods.models import Product  # Импортируем из goods

# ... ваш существующий код views для корзины
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
        return redirect('core:login')
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    if cart:
        # Пытаемся найти товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            # Если товар уже был в корзине - увеличиваем количество
            cart_item.quantity += 1
            cart_item.save()
            
        messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    else:
        messages.error(request, 'Для добавления в корзину необходимо авторизоваться')
    
    # Возвращаем на ту же страницу, откуда пришел пользователь
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('core:product_list')

def cart_add_with_quantity(request, product_id):
    """Добавление товара в корзину с указанием количества"""
    if not request.user.is_authenticated:
        messages.info(request, 'Для добавления товаров в корзину необходимо авторизоваться')
        return redirect('core:login')
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        
        if cart and quantity > 0:
            # Пытаемся найти товар в корзине
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Если товар уже был в корзине - увеличиваем количество
                cart_item.quantity += quantity
                cart_item.save()
                
            messages.success(request, f'Товар "{product.name}" ({quantity} шт.) добавлен в корзину')
        else:
            messages.error(request, 'Ошибка при добавлении товара в корзину')
        
        return redirect('core:product_detail', product_id=product_id)
    
    return redirect('core:product_list')

def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    if not request.user.is_authenticated:
        messages.info(request, 'Для управления корзиной необходимо авторизоваться')
        return redirect('core:login')
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    if cart:
        CartItem.objects.filter(cart=cart, product=product).delete()
        messages.success(request, f'Товар "{product.name}" удален из корзины')
    
    return redirect('core:cart_detail')

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

def cart_clear(request):
    """Полная очистка корзины"""
    if not request.user.is_authenticated:
        messages.info(request, 'Для управления корзиной необходимо авторизоваться')
        return redirect('core:login')
    
    cart = get_cart(request)
    if cart:
        cart.items.all().delete()
        messages.success(request, 'Корзина очищена')
    
    return redirect('core:cart_detail')

# ФУНКЦИИ АУТЕНТИФИКАЦИИ

# Контекстный процессор для корзины
def get_user_cart(request):
    """Получает корзину текущего пользователя для контекста"""
    if request.user.is_authenticated:
        try:
            return Cart.objects.get(user=request.user, is_active=True)
        except Cart.DoesNotExist:
            return None
    return None

