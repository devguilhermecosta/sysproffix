from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . models import Hospital
from . forms import HospitalRegisterForm
from utils.decorators import only_user_admin


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
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
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
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
                'title': 'cadastrar novo hospital',
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


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class HospitalDetailsView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        hospital = get_object_or_404(Hospital, pk=pk)
        session = self.request.session.get('hospital-edit', None)
        form = HospitalRegisterForm(session, instance=hospital)

        return render(
            request=self.request,
            template_name='hospital/pages/details.html',
            context={
                'form': form,
                'title': 'editar hospital',
                'button_value': 'salvar',
                'hospital': hospital,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        hospital = get_object_or_404(Hospital, pk=pk)
        post = self.request.POST
        self.request.session['hospital-edit'] = post
        form = HospitalRegisterForm(post, instance=hospital)

        if form.is_valid():
            form.save()
            del self.request.session['hospital-edit']
            messages.success(
                self.request,
                'Registro salvo com sucesso',
            )
            return redirect(reverse('hospital:list'))

        messages.error(
            self.request,
            'Existem erros no formulário',
        )

        return redirect(reverse('hospital:details', args=(pk,)))


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class HospitalDeleteView(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        hospital = get_object_or_404(Hospital, pk=pk)

        if not self.request.user.is_staff:  # type: ignore
            messages.error(
                self.request,
                'Você não tem permissão para executar esta operação.',
            )
            return redirect(reverse('hospital:details', args=(pk,)))

        hospital.delete()

        messages.success(
            self.request,
            'Registro deletado com sucesso',
        )

        return redirect(
            reverse('hospital:list')
        )
