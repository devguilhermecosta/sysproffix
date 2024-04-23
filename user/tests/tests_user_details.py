from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.hospital import create_hospital
from django.urls import reverse
from django.contrib.auth import get_user_model
from parameterized import parameterized  # type: ignore


UserModel = get_user_model()


class UserDetailsTests(TestCaseWithLogin):
    base_url = reverse('users:details', args=(1,))

    def test_user_must_be_loged_in(self) -> None:
        """
            if the uer is not authenticated, will be redirected
            to login page.
        """
        response = self.client.get(self.base_url)

        self.assertRedirects(
            response=response,
            expected_url='/?next=/usuarios/1/details/',
            status_code=302,
        )

    def test_should_show_permission_denied_if_the_user_is_not_admin(self) -> None:  # noqa: E501
        """
            to access the view the user must be an administrator
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 403)

    def test_should_return_status_404_if_user_not_found(self) -> None:
        self.make_login()
        response = self.client.get(reverse('users:details', args=(10,)))
        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        'Nome:',
        'Sobrenome:',
        'Email:',
        'Usuário de hospital',
        'Administrador',
        'Desenvolvedor',
        'Hospital:',
        'editar usuário',
        'jhon',  # user data
        'dhoe',  # user data
        'email@email.com',  # user data
        'Hospital Health',  # user data
        'salvar',
    ])
    def test_should_show_the_correct_content(self, text: str) -> None:
        """
            this test checks if the content of the page
            is correct.
        """
        user, _ = self.make_login()
        hospital = create_hospital(name='Hospital Health')
        user.hospital = hospital  # type: ignore
        user.save()

        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")

        self.assertIn(text, content)

    @parameterized.expand([
        ('first_name', '', 'campo obrigatório'),
        ('last_name', '', 'campo obrigatório'),
        ('email', '', 'campo obrigatório'),
        ('hospital', '', 'campo obrigatório'),
    ])
    def test_must_show_error_messages(self, field: str, value: str, error: str) -> None:  # noqa: E501
        """
            if exists erros on register form, the form
            must should display error messages
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

        content = response.content.decode("utf-8")

        self.assertIn(error, content)
        self.assertIn('Existem erros no formulário', content)
        self.assertRedirects(
            response=response,
            expected_url='/usuarios/1/details/',
            status_code=302,
        )

    def test_should_save_all_changes(self) -> None:
        """ User data must be updated """

        # the user original data is:
        # first_name=jhon, last_name=doe, email=email@email.com, hospital=None
        self.make_login()

        # create Hospital instance
        create_hospital('Hospital Maria da Silva')

        form_update_data = {
            'first_name': 'maria',
            'last_name': 'da silva',
            'email': 'maria@email.com',
            'is_hospital_user': True,
            'is_admin': True,
            'is_staff': True,
            'hospital': 1,
        }

        response = self.client.post(
            self.base_url,
            form_update_data,
            follow=True,
        )

        content = response.content.decode("utf-8")

        # get the user instance
        user = UserModel.objects.get(pk=1)

        self.assertEqual(user.first_name,  # type: ignore
                         form_update_data['first_name'])
        self.assertEqual(user.last_name,  # type: ignore
                         form_update_data['last_name'])
        self.assertEqual(user.email,  # type: ignore
                         form_update_data['email'])
        self.assertEqual(user.is_admin,  # type: ignore
                         form_update_data['is_admin'])
        self.assertEqual(user.is_staff,  # type: ignore
                         form_update_data['is_staff'])  # type: ignore
        self.assertEqual(user.is_hospital_user,  # type: ignore
                         form_update_data['is_hospital_user'])

        self.assertIn('Usuário salvo com sucesso', content)

        self.assertRedirects(
            response=response,
            expected_url=self.base_url,
            status_code=302,
        )
