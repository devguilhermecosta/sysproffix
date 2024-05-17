from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from utils.decorators import only_user_admin


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class OnlyAdminBaseView(View):
    ...


@method_decorator(
    [
        login_required(redirect_field_name='next', login_url='/'),
        only_user_admin,
    ],
    name='dispatch',
)
class OnlyAdminListView(ListView):
    ...
