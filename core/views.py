# core/views.py
from django.shortcuts import render
from goods.models import Product, Category  # Импортируем из goods

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