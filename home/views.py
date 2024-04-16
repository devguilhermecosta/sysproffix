from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render


class LoginView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            template_name='home/pages/login.html',
        )
