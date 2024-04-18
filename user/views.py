from django.views import View
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
                'users': users
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

        form = UserRegisterForm()

        return render(
            self.request,
            'user/pages/new_user.html',
            context={
                'form': form,
            }
        )
