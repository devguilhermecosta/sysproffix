from django.views import View
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from user.forms import UserRegisterForm


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class UserListView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user_model = get_user_model()
        users = user_model.objects.all()

        return render(
            self.request,
            'user/pages/users.html',
            context={
                'users': users,
            }
        )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class UserCreateView(View):
    def get(self, *args, **kwargs) -> HttpResponse:

        session = self.request.session.get('user-register', None)
        form = UserRegisterForm(session)

        return render(
            self.request,
            'user/pages/new_user.html',
            context={
                'form': form,
                'title': 'cadastrar novo usuário',
                'url': reverse('users:new'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['user-register'] = post
        form = UserRegisterForm(data=post)

        if form.is_valid():
            form.save()

            del self.request.session['user-register']

            messages.success(
                self.request,
                'Usuário registrado com sucesso'
            )

            return redirect(reverse('users:list'))

        messages.error(
            self.request,
            'Existem erros no formulário'
        )

        return redirect(reverse('users:new'))


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class UserDetailView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        user = get_object_or_404(get_user_model(), pk=pk)
        session = self.request.session.get('user-edit', None)
        form = UserRegisterForm(session, instance=user)

        return render(
            self.request,
            'user/pages/details.html',
            context={
                'user_detail': user,
                'form': form,
                'title': 'editar usuário',
                'button_value': 'salvar',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        user = get_object_or_404(get_user_model(), pk=pk)
        post = self.request.POST
        self.request.session['user-edit'] = post
        form = UserRegisterForm(post, instance=user)

        if form.is_valid():
            form.save()

            del self.request.session['user-edit']

            messages.success(
                self.request,
                'Usuário salvo com sucesso'
            )

        else:
            messages.error(
                self.request,
                'Existem erros no formulário'
            )

        return redirect(reverse('users:details', args=(user.pk,)))


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class UserDeleteView(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        user = get_object_or_404(get_user_model(), pk=pk)
        user.delete()

        messages.success(
            self.request,
            'Usuário deletado com sucesso'
        )

        return redirect(reverse('users:list'))

# TODO antes de continuar, criar todos os testes de usuário.
# TODO preciso criar o sistema de geração automática de senha e enviar por e-mail  # noqa: E501
