from django.test import TestCase
from django.urls import reverse
from django.core import mail
from parameterized import parameterized  # type: ignore
from utils.for_test.auth.user import create_superuser


class ResetPasswordTests(TestCase):
    base_url = reverse('users:reset-password')

    @parameterized.expand([
        'e-mail',
        'Digite seu email...',
        'recuperar senha',
    ])
    def test_must_render_the_corret_content_on_get_request(self, txt: str) -> None:  # noqa: E501
        response = self.client.get(self.base_url)
        reset_password_form = response.context['form']

        self.assertIn(
            txt,
            response.content.decode("utf-8")
        )
        self.assertTrue(reset_password_form)

    def test_must_returns_error_message_if_not_email(self) -> None:
        response = self.client.post(
            self.base_url,
            follow=True,
        )

        content = response.content.decode("utf-8")

        self.assertIn('Existem erros no formulário', content)
        self.assertIn('Campo obrigatório', content)
        self.assertRedirects(
            response,
            self.base_url,
            302,
        )

    def test_must_returns_error_message_if_not_user(self) -> None:
        response = self.client.post(
            self.base_url,
            {'email': 'jhon@email.com'},
            follow=True,
        )

        content = response.content.decode("utf-8")

        self.assertIn('Existem erros no formulário', content)
        self.assertIn('Usuário não cadastrado', content)
        self.assertRedirects(
            response,
            self.base_url,
            302,
        )

    def test_must_sent_an_email_with_the_new_password(self) -> None:
        create_superuser('jhon', 'doe,', 'jhon@email.com', '123')

        response = self.client.post(
            self.base_url,
            {'email': 'jhon@email.com'},
            follow=True,
        )

        email = mail.outbox

        self.assertIn(
            'E-mail enviado com sucesso',
            response.content.decode("utf-8")
        )
        self.assertEqual(len(email), 1)
        self.assertEqual(email[0].subject, 'Recuperação de senha')
        self.assertIn(
            'Você está recebendo este e-mail pois solicitou a recuperação de sua senha de acesso.',  # noqa: E501
            email[0].body,
        )
