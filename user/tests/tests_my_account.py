from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.hospital import create_hospital
from django.urls import reverse
from parameterized import parameterized  # type: ignore
from datetime import date


class MyAccountTests(TestCaseWithLogin):
    base_url = reverse('users:account')

    def test_the_user_must_be_logged_in(self) -> None:
        """
            if the user is not logged in, he will redirected
            to login page.
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/usuarios/minha-conta/',
            status_code=302,
        )

    @parameterized.expand([
        'nome',
        'email',
        'instituição',
        'desde',
        'Jhon Dhoe',  # full name
        'email@email.com',  # email
        str(date.today().strftime('%d/%m/%Y')),  # created_at
        'Hospital Health',
        'minha conta',
        'nova senha',
        'repita a senha',
        'cadastrar nova senha',
    ])
    def test_should_render_the_correct_content(self, txt: str) -> None:
        """
            it should render logged in user data.
        """
        hospital = create_hospital('hospital health')
        user, _ = self.make_login()
        user.hospital = hospital  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertIn(
            txt,
            response.content.decode("utf-8"),
        )

    @parameterized.expand([
        ('password', '', 'campo obrigatório'),
        ('password', '123', (
            'A senha precisa ter pelo menos:\n'
            '- oito catacteres\n'
            '- uma letra maíuscula\n'
            '- uma letra minúscula\n'
            '- um número.'
        )),
        ('password_confirm', '', 'campo obrigatório'),
    ])
    def test_should_return_error_messages(self, field, value, msg) -> None:
        """
            if the user try change your password, the form
            must render error messages when errors.
        """
        self.make_login()

        form_data = {
            field: value,
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )

        self.assertIn(
            msg,
            response.content.decode("utf-8"),
        )
        self.assertIn(
            'Existem erros no formulário',
            response.content.decode("utf-8"),
        )
        self.assertRedirects(
            response=response,
            expected_url=self.base_url,
            status_code=302,
        )

    def test_should_update_the_user_password(self) -> None:
        """
            when the user password is updated, a success message
            is displayed.
        """
        self.make_login()

        password = 'Abc123@@'
        form_data = {
            'password': password,
            'password_confirm': password,
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )

        self.assertIn(
            'Senha alterada com sucesso',
            response.content.decode("utf-8"),
        )
        self.assertRedirects(
            response=response,
            expected_url=self.base_url,
            status_code=302,
        )
