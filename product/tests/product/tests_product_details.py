from django.urls import reverse
from utils.for_test.auth.authentication import TestCaseWithLogin
from parameterized import parameterized  # type: ignore
from utils.for_test.models import product


class ProductDetailTests(TestCaseWithLogin):
    base_url = reverse('products:details', args=(1,))

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/1/detail/',
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

    def test_should_returns_404_if_the_product_dont_exists(self) -> None:
        self.make_login()
        respose = self.client.get(self.base_url)
        self.assertEqual(respose.status_code, 404)

    @parameterized.expand([
        'editar produto',
        'Grupo',
        'Código',
        '1234',  # code
        'Descrição',
        'product-1',  # name
        'group',  # group name
        'salvar',
    ])
    def test_should_render_the_product_data(self, text: str) -> None:
        self.make_login()
        product.create_product(code='1234', name='product-1')

        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('group', '', 'Este campo é obrigatório'),
        ('code', '', 'Este campo é obrigatório'),
        ('code', '12345', 'já existe um produto com este código'),
        ('name', '', 'Este campo é obrigatório'),
    ])
    def test_should_render_error_messages(self, field: str, value: str, msg: str) -> None:  # noqa: E501
        self.make_login()
        product.create_product(code='1234', name='product-1')
        product.create_product(code='12345', name='product-1')

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

    def test_should_save_the_product(self) -> None:
        self.make_login()
        product.create_product(code='1234', name='product-1')

        product_data = {
            'group': 1,
            'code': '1234',
            'name': 'product name changed'
        }

        response = self.client.post(
            self.base_url,
            product_data,
            follow=True
        )

        self.assertIn(
            'Produto salvo com sucesso',
            response.content.decode("utf-8"),
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('products:list'),
            status_code=302,
        )
