# carts/context_processors.py
from .models import Cart

def cart_context(request):
    """Добавляет корзину в контекст всех шаблонов"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
            return {'cart': cart}
        except Cart.DoesNotExist:
            return {'cart': None}
    return {'cart': None}