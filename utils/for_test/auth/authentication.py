from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import AbstractUser
from .user import create_superuser


class TestCaseWithLogin(TestCase):
    authentication_base_url = reverse('home:authentication')

    def make_login(self,
                   f_name: str = 'jhon',
                   l_name: str = 'dhoe',
                   email: str = 'email@email.com',
                   password: str = '123456',
                   ) -> tuple[AbstractUser, HttpResponse]:
        """
            Authenticate and create the user.
        """

        user = create_superuser(f_name, l_name, email, password)

        response = self.client.post(
            self.authentication_base_url,
            {
                'username': email,
                'password': password,
            },
            follow=True,
        )

        return user, response
