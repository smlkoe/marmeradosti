from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm

User = get_user_model()
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
