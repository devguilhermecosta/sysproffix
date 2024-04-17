from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized  # type: ignore
from utils.for_test.auth.user import create_superuser


class HomeTests(TestCase):
    login_base_url = 'home:login'
    authentication_base_url = 'home:authentication'

    def test_home_loads_correct_template(self) -> None:
        response = self.client.get(reverse(self.login_base_url))

        self.assertTemplateUsed(response, 'home/pages/login.html')

    @parameterized.expand([
        ("Digite seu e-mail..."),
        ("Digite sua senha..."),
        ("acessar painel"),
    ])
    def test_home_loads_correct_content(self, text: str) -> None:
        response = self.client.get(reverse(self.login_base_url))
        content = response.content.decode("utf-8")

        self.assertIn(
            text,
            content
        )

    def test_home_returns_error_message_if_not_user(self) -> None:
        """
            Must returns error message if invalid user or password.
        """
        response = self.client.post(
            reverse(self.authentication_base_url),
            {
                'username': 'any',
                'password': 'any',
            },
            follow=True
        )

        self.assertIn(
            "Usuário ou senha inválidos.",
            response.content.decode("utf-8"),
        )

    def test_home_returns_success_message_if_user(self) -> None:
        """
            Must returns error message if invalid user or password.
        """

        create_superuser('jhon', 'dhoe', 'email@email.com', '123456')

        response = self.client.post(
            reverse(self.authentication_base_url),
            {
                'username': 'email@email.com',
                'password': '123456',
            },
            follow=True
        )

        self.assertIn(
            "Login realizado com sucesso",
            response.content.decode("utf-8"),
        )

    def test_home_show_message_if_the_is_authenticate(self) -> None:
        """
            If the user is already authenticated and tries to access
            the login page, a message will be displayed.
        """

        create_superuser('jhon', 'dhoe', 'email@email.com', '123456')

        # login
        self.client.post(
            reverse(self.authentication_base_url),
            {
                'username': 'email@email.com',
                'password': '123456',
            },
            follow=True
        )

        response = self.client.post(
            reverse(self.login_base_url),
            follow=True,
        )

        content = response.content.decode("utf-8")

        self.assertIn(
            "Você está logado como",
            content,
        )
        self.assertIn(
            "jhon dhoe",
            content,
        )
