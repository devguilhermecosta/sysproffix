from django.http import HttpResponse, HttpRequest
from django.core.exceptions import PermissionDenied
from typing import Callable


def only_user_admin(func: Callable[[HttpRequest, tuple, dict], HttpResponse]) -> Callable:  # noqa: E501
    """If the user is not an administrator, raises Forbidden (403)."""
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        if not user.is_admin:  # type: ignore
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrapper
