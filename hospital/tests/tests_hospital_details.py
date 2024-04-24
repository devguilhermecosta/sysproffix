from utils.for_test.auth.authentication import TestCaseWithLogin
from django.urls import reverse
from utils.for_test.models.hospital import create_hospital
from parameterized import parameterized  # type: ignore
from hospital.models import Hospital


class HospitalDetailsTests(TestCaseWithLogin):
    base_url = reverse('hospital:details', args=(1,))

    def test_the_user_must_be_authenticated(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/hospitais/1/details/',
            status_code=302,
        )

    def test_the_user_must_be_an_administrator(self) -> None:
        """
            if the user is not an administrator, he will
            receive a status code 302 (Forbiden).
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 403)

    def test_should_returns_status_code_404(self) -> None:
        """
            if the hospital not exists, the user must receive
            a status code 404.
        """
        self.make_login()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        'Hospital',
        'São Paulo',
        'SP',
        'editar hospital',
        'salvar',
        'deletar',
    ])
    def test_should_render_the_correct_content(self, txt: str) -> None:
        """
            the hospital infos must be correct.
        """
        create_hospital()
        self.make_login()

        response = self.client.get(self.base_url)

        self.assertIn(
            txt,
            response.content.decode("utf-8"),
        )

    @parameterized.expand([
        ('name', '', 'campo obrigatório'),
        ('name', 'hospital-2', 'Hospital com este Nome já existe.'),
        ('city', '', 'campo obrigatório'),
        ('state', '', 'campo obrigatório'),
    ])
    def test_the_form_must_returns_error_messages(self, field: str, txt: str, msg: str) -> None:  # noqa: E501
        """
            on post request the form must render error messages
            when erros.
        """
        for i in range(3):
            create_hospital(name=f'hospital-{i}')

        self.make_login()

        form_data = {
            field: txt,
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

    def test_should_change_hospital_data(self) -> None:
        """
            if the form is ok, the hospital data must be changed.
        """
        create_hospital(name='hospital', city='são paulo', state='sp')
        self.make_login()
        form_data = {
            'name': 'hospital changed',
            'city': 'new york',
            'state': 'ny'
        }

        response = self.client.post(
            self.base_url,
            form_data,
            follow=True,
        )
        content = response.content.decode("utf-8")

        hospital = Hospital.objects.get(id=1)

        self.assertEqual(hospital.name, form_data['name'])
        self.assertEqual(hospital.city, form_data['city'])
        self.assertEqual(hospital.state, form_data['state'])

        self.assertIn(
            'Registro salvo com sucesso',
            content,
        )

        self.assertRedirects(
            response=response,
            expected_url='/hospitais/list/',
            status_code=302,
        )
