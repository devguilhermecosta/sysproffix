from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from typing import Any
from utils.for_test.auth.user import create_superuser
from utils.decorators.decorators import only_user_admin


# create a simple function for test
@only_user_admin
def func_for_test(request: HttpRequest, *args, **kwargs) -> Any:
    if args or kwargs:
        return f'function returned with: {args} - {kwargs}'
    return 'function returned'


class TestOnlyUserAdminDecorator(TestCase):
    def setUp(self) -> None:
        self.user = create_superuser('jhon', 'doe', 'j@email.com', '123')
        return super().setUp()

    def test_should_raises_permissiondenied(self) -> None:
        """
            when the user is not an administrator, the decorator
            should raises PermissionDenied.
        """
        with self.assertRaises(PermissionDenied):
            self.user.is_admin = False  # type: ignore
            self.user.save()
            request = HttpRequest()
            request.user = self.user

            func_for_test(request)

    def test_should_return_the_function(self) -> None:
        """
            when the user is an administrator, the decorator should
            return the function itself.
            in this case, when the function is returned by the decorator,
            the 'function returned' text is returned.
        """
        request = HttpRequest()
        request.user = self.user

        func = func_for_test(request)

        self.assertEqual(func, 'function returned')

    def test_must_accept_args_and_kwargs(self) -> None:
        """
            When the decorated function receives arguments,
            these arguments must be passed to the returned function.
        """
        request = HttpRequest()
        request.user = self.user
        func = func_for_test(request, 10, 'name=test')

        self.assertEqual(
            func, "function returned with: (10, 'name=test') - {}"
        )
