from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Hospital
from . forms import HospitalRegisterForm


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='/',
                   ),
    name='dispatch',
)
class HospitalListView(View):
    def get(self, *args, **kwargs) -> HttpResponse:

        hospital_list = Hospital.objects.all()

        return render(
            self.request,
            'hospital/pages/list.html',
            context={
                'hospitals': hospital_list
            }
        )


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='/',
                   ),
    name='dispatch',
)
class HospitalRegisterView(View):
    def get(self, *args, **kwargs) -> HttpResponse:

        session = self.request.session.get('hospital-register', None)

        form = HospitalRegisterForm(session)

        return render(
            self.request,
            'hospital/pages/new.html',
            context={
                'form': form,
                'title': 'cadastrar nova hospital',
                'url': reverse('hospital:create'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['hospital-register'] = post
        form = HospitalRegisterForm(data=post)

        if form.is_valid():
            form.save()
            messages.success(
                self.request,
                'Cadastro realizado com sucesso',
            )

            del self.request.session['hospital-register']

            return redirect(reverse('hospital:list'))

        messages.error(
            self.request,
            'Existem erros no formulário',
        )

        return redirect(reverse('hospital:new'))
