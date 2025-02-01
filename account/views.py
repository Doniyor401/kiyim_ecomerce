from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Перенаправление на страницу, куда пользователь пытался попасть
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, "Неверные данные для входа. Попробуйте снова.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)  # Завершаем сессию пользователя
    return redirect('home')
