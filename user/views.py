from django.views import View
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login
from user.forms import UserRegisterForm, ChangePasswordForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from utils.decorators import only_user_admin
from utils.strings.password import generate_password
from utils.log import LogMixin


UserModel = get_user_model()


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
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
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class UserCreateView(View, LogMixin):
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
            user_email = form.cleaned_data['email']
            user = UserModel.objects.get(email=user_email)

            password = generate_password()
            user.set_password(password)
            user.save()

            del self.request.session['user-register']

            messages.success(
                self.request,
                'Usuário registrado com sucesso'
            )

            try:
                send_mail(
                    'Registro realizado com sucesso',
                    strip_tags(
                        render_to_string('user/pages/email.html', context={
                            'new_user': user,
                            'password': password,
                            'link': get_current_site(self.request).domain,
                        })
                    ),
                    settings.EMAIL_HOST_USER,
                    [user.email],  # type: ignore
                    fail_silently=False,
                )
                self.log_success(
                    f'email enviado com sucesso para {user.email}'  # type: ignore  # noqa: E501
                )
            except Exception as error:
                self.log_error(f'erro ao enviar o email para {user.email}: {error}')  # type: ignore  # noqa: E501

            return redirect(reverse('users:list'))

        messages.error(
            self.request,
            'Existem erros no formulário'
        )

        return redirect(reverse('users:new'))


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
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
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
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


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
    ],
    name='dispatch',
)
class MyAccountView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('change-password', None)
        form = ChangePasswordForm(session)

        return render(
            self.request,
            'user/pages/my_account.html',
            context={
                'form': form,
                'url': reverse('users:change-password'),
                'button_value': 'cadastrar nova senha'
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        post = self.request.POST
        self.request.session['change-password'] = post
        form = ChangePasswordForm(post)

        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            user.set_password(password)
            user.save()

            del self.request.session['change-password']

            user_auth = authenticate(self.request,
                                     username=user.email,  # type: ignore
                                     password=password,
                                     )
            login(self.request, user_auth)

            messages.success(
                self.request,
                'Senha alterada com sucesso'
            )

        else:
            messages.error(
                self.request,
                'Existem erros no formulário',
            )

        return redirect(reverse('users:account'))


# TODO criar o sistema de recuperação de senha
