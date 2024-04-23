from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.hospital import create_hospital
from django.urls import reverse
from parameterized import parameterized  # type: ignore


class UserCreateTests(TestCaseWithLogin):
    base_url = reverse('users:new')

    def test_user_must_be_loged_in(self) -> None:
        """
            the user must be redirected to login page
            if not authenticated.
        """
        response = self.client.get(self.base_url)

        self.assertRedirects(
            response=response,
            expected_url='/?next=/usuarios/new/',
            status_code=302,
        )

    def test_must_show_permission_denied(self) -> None:
        """
            If the user is not an administrator, he will
            receive a forbidden message (403)
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 403)

    @parameterized.expand([
        'Nome:',
        'Sobrenome:',
        'Email:',
        'Usuário de hospital',
        'Administrador',
        'Desenvolvedor',
        'Hospital:',
        'cadastrar novo usuário',
        'cadastrar',
        'action="/usuarios/new/',  # link to post request
    ])
    def test_must_show_the_correct_content(self, text: str) -> None:
        """
            this test checks if the content of the page
            is correct.
        """
        self.make_login()

        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")

        self.assertIn(text, content)

    @parameterized.expand([
        ('first_name', '', 'campo obrigatório'),
        ('last_name', '', 'campo obrigatório'),
        ('email', '', 'campo obrigatório'),
        ('email', 'email@email.com', 'e-mail já cadastrado'),
        ('hospital', '', 'campo obrigatório'),
    ])
    def test_must_show_error_messages(self, field: str, value: str, error: str) -> None:  # noqa: E501
        """
            if exists erros on register form, the form
            must should display error messages
        """
        self.make_login(email='email@email.com')

        form_data = {
            field: value,
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )

        content = response.content.decode("utf-8")

        self.assertIn(error, content)
        self.assertIn('Existem erros no formulário', content)
        self.assertRedirects(
            response=response,
            expected_url='/usuarios/new/',
            status_code=302,
        )

    def test_should_register_a_new_user(self) -> None:
        self.make_login()
        create_hospital()

        form_data = {
            'first_name': 'jhon',
            'last_name': 'doe',
            'email': 'jhon@email.com',
            'password': '123456',
            'hospital': 1,  # this is a select input
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )

        content = response.content.decode("utf-8")

        self.assertIn(
            "Usuário registrado com sucesso",
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url='/usuarios/list/',
            status_code=302,
        )
