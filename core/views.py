from django.shortcuts import render
from .models import Product, Category

def home(request):
    """Главная страница"""
    # Получаем только активные продукты
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