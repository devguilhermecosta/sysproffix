from django.urls import reverse
from utils.for_test.auth.authentication import TestCaseWithLogin
from parameterized import parameterized  # type: ignore
from utils.for_test.models import product


class ProductCreateTests(TestCaseWithLogin):
    base_url = reverse('products:new')

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/new/',
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
        'novo produto',
        'Grupo',
        'Código',
        'Descrição',
        'cadastrar'
    ])
    def test_should_render_the_product_form(self, text: str) -> None:
        self.make_login()
        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('group', '', 'Este campo é obrigatório'),
        ('code', '', 'Este campo é obrigatório'),
        ('code', '1234', 'já existe um produto com este código'),
        ('name', '', 'Este campo é obrigatório'),
    ])
    def test_should_render_error_messages(self, field: str, value: str, msg: str) -> None:  # noqa: E501
        self.make_login()
        product.create_product(code='1234')

        product_data = {
            field: value
        }

        response = self.client.post(self.base_url, product_data, follow=True)
        content = response.content.decode("utf-8")

        self.assertIn(
            msg,
            content,
        )
        self.assertIn(
            'Existem erros no formulário',
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url=self.base_url,
            status_code=302,
        )

    def test_should_create_a_new_product(self) -> None:
        """
            if the product is created, a success message must be displayed.
        """
        self.make_login()

        product.create_product_group()

        product_data = {
            'group': 1,
            'code': '1234',
            'name': 'product'
        }

        response = self.client.post(
            self.base_url,
            product_data,
            follow=True
        )

        self.assertIn(
            'Produto criado com sucesso',
            response.content.decode("utf-8"),
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('products:list'),
            status_code=302,
        )
