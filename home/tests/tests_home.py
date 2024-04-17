from django.test import TestCase
from django.urls import reverse, resolve
from parameterized import parameterized  # type: ignore
from home import views


class HomeTests(TestCase):
    base_url = 'home:login'

    def test_home_url_is_correct(self) -> None:
        url = reverse(self.base_url)

        self.assertEqual(url, '/')

    def test_home_uses_correct_view(self) -> None:
        response = resolve(reverse(self.base_url))

        self.assertEqual(
            response.func.view_class,  # type: ignore
            views.LoginView,
            )

    def test_home_loads_correct_template(self) -> None:
        response = self.client.get(reverse(self.base_url))

        self.assertTemplateUsed(response, 'home/pages/login.html')

    @parameterized.expand([
        ("Digite seu e-mail..."),
        ("Digite sua senha..."),
        ("acessar painel"),
    ])
    def test_home_loads_correct_content(self, text: str) -> None:
        response = self.client.get(reverse(self.base_url))
        content = response.content.decode("utf-8")

        self.assertIn(
            text,
            content
        )
