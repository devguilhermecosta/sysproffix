from django.urls import reverse
from parameterized import parameterized  # type: ignore
from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.product import create_product_group


class ProductGroupRegisterTests(TestCaseWithLogin):
    base_url = reverse('products:group_register')

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/groups/register/',
            status_code=302,
        )

    def test_the_user_must_be_an_administrator(self) -> None:
        """
            if the user is not an admin, he will receives 403
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 403)

    @parameterized.expand([
        'novo grupo',
        'Descrição',
        'cadastrar',
    ])
    def test_should_render_the_correct_content(self, txt: str) -> None:
        self.make_login()
        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")
        self.assertIn(txt, content)

    @parameterized.expand([
        ('name', '', 'Este campo é obrigatório'),
        ('name', 'group-1', 'já existe um grupo com este nome'),
    ])
    def test_should_display_error_messages(self, field: str, value: str, msg: str) -> None:  # noqa: E501
        self.make_login()
        create_product_group(name='group-1')

        group_data = {
            field: value,
        }

        response = self.client.post(self.base_url, group_data, follow=True)
        content = response.content.decode("utf-8")

        self.assertIn(msg, content)
        self.assertIn('Existem erros no formulário', content)
        self.assertRedirects(
            response=response,
            expected_url=self.base_url,
            status_code=302,
        )

    def test_should_create_a_new_group(self) -> None:
        self.make_login()

        group_data = {
            'name': 'group-1',
        }

        response = self.client.post(self.base_url, group_data, follow=True)
        content = response.content.decode("utf-8")

        self.assertIn('Grupo criado com sucesso', content)
        self.assertRedirects(
            response=response,
            expected_url=reverse('products:group_list'),
            status_code=302,
        )
