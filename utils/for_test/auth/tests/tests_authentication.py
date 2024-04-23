from utils.for_test.auth.authentication import TestCaseWithLogin
from django.contrib.auth import get_user_model
from django.http import HttpResponse


UserModel = get_user_model()


class TestsOfTestCaseWithLoginClass(TestCaseWithLogin):
    def test_must_create_a_new_user(self) -> None:
        """
            the make_login method should create a new superuser.
        """
        user, _ = self.make_login()
        self.assertTrue(isinstance(user, UserModel))

    def test_must_authenticate_the_user(self) -> None:
        """
            the user must be authenticated.
        """
        user, _ = self.make_login()
        self.assertTrue(user.is_authenticated)

    def test_should_return_an_instance_of_http_response(self) -> None:
        _, response = self.make_login()
        self.assertTrue(isinstance(response, HttpResponse))
