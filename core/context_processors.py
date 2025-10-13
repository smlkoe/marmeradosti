from .models import Cart

def cart(request):
    """
    Контекст-процессор для отображения корзины на всех страницах
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if cart:
            return {'cart': cart}
    return {'cart': None}