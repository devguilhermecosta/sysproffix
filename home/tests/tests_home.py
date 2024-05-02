from django.urls import reverse
from django.test import TestCase
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
        ("esqueci minha senha"),
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

    def test_home_must_redirects_to_main_page(self) -> None:
        """
            if the user is authenticated, he will redirected to main page
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

        response = self.client.get(
            reverse(self.login_base_url),
            follow=True,
        )

        self.assertRedirects(
            response=response,
            expected_url='/home/',
            status_code=302
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
