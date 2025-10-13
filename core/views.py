from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Cart, CartItem

def home(request):
    """Главная страница"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
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

@login_required
def cart_add(request, product_id):
    """Добавление товара в корзину"""
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
    
    return redirect('core:product_list')

@login_required
def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    
    if cart:
        CartItem.objects.filter(cart=cart, product=product).delete()
        messages.success(request, f'Товар "{product.name}" удален из корзины')
    
    return redirect('core:cart_detail')

@login_required
def cart_detail(request):
    """Страница просмотра корзины"""
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