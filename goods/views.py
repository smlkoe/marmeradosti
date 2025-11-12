from django.shortcuts import render, get_object_or_404
from .models import Product, Category
def product_list(request):
    """Страница со списком всех продуктов"""
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id, is_active=True)
        try:
            current_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            current_category = None
    else:
        products = Product.objects.filter(is_active=True)
        current_category = None
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'core/product_list.html', context)
def category_products(request, category_id):
    """Страница товаров конкретной категории"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_active=True)
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'core/product_list.html', context)

def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    categories = Category.objects.all()
    
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'core/product_detail.html', context)