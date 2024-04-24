from utils.for_test.auth.authentication import TestCaseWithLogin
from django.urls import reverse
from parameterized import parameterized  # type: ignore
from utils.for_test.models.hospital import create_hospital
from hospital.models import Hospital


class HospitalRegisterTests(TestCaseWithLogin):
    base_url = reverse('hospital:new')

    def test_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be logged in.
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/hospitais/new/',
            status_code=302,
        )

    def test_user_must_be_an_administrator(self) -> None:
        """
            if the user is not and administrator, the
            status code must be 403 (Forbiden).
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 403)

    @parameterized.expand([
        'cadastrar novo hospital',
        'Nome:',
        'Cidade:',
        'Estado:',
        'cadastrar',
        'action="/hospitais/create/"'  # form action
    ])
    def test_should_render_the_correct_content(self, text: str) -> None:
        self.make_login()
        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")
        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('name', '', 'campo obrigatório'),
        ('name', 'hospital', 'Hospital com este Nome já existe'),
        ('city', '', 'campo obrigatório'),
        ('state', '', 'campo obrigatório'),
    ])
    def test_should_return_error_messages(self, field: str, text: str, msg: str) -> None:  # noqa: E501
        """
            on post request the form must return errors
            messages when errors.
        """
        create_hospital(name='hospital')
        self.make_login()
        form_data = {
            field: text,
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )
        content = response.content.decode("utf-8")

        self.assertIn(
            'Existem erros no formulário',
            content,
        )
        self.assertIn(
            msg,
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url=self.base_url,
            status_code=302,
        )

    def test_should_create_a_new_hospital(self) -> None:
        """
            on post request a new hospital must be created
            if all data is ok.
        """
        self.make_login()
        form_data = {
            'name': 'hospital',
            'city': 'new york',
            'state': 'ny'
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )

        hospital = Hospital.objects.all()

        self.assertTrue(hospital.exists())
        self.assertRedirects(
            response=response,
            expected_url='/hospitais/list/',
            status_code=302,
        )
        self.assertIn(
            'Cadastro realizado com sucesso',
            response.content.decode("utf-8"),
        )
