from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.views import OnlyAdminBaseView


class LoginView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user

        if user.is_authenticated:
            return redirect(
                reverse('home:main')
            )

        return render(
            self.request,
            template_name='home/pages/login.html',
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            messages.success(self.request, 'Login realizado com sucesso')
            login(self.request, user=user)
            return redirect(reverse('home:main'))
        else:
            messages.error(self.request, 'Usuário ou senha inválidos.')
            return redirect(reverse("home:login"))


class LogoutView(OnlyAdminBaseView):
    def get(self, *args, **kwargs) -> HttpResponse:
        logout(self.request)
        messages.success(self.request, 'Logout realizado com sucesso')
        return redirect(reverse('home:login'))


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class HomeView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'home/pages/main.html',
        )
