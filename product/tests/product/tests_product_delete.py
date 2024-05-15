from django.urls import reverse
from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models import product


class ProductDeleteTests(TestCaseWithLogin):
    base_url = reverse('products:delete', args=(1,))

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.post(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/1/delete/',
            status_code=302,
        )

    def test_the_user_must_be_an_administrator(self) -> None:
        """
            if the user is not an admin, he will receives 403
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.post(self.base_url)

        self.assertEqual(response.status_code, 403)

    def test_should_returns_404_if_the_product_dont_exists(self) -> None:
        self.make_login()
        respose = self.client.post(self.base_url)
        self.assertEqual(respose.status_code, 404)

    def test_should_render_error_message(self) -> None:
        """
            it should render error message if the product has a
            ProductItem.
        """
        self.make_login()
        product.create_product_item()

        response = self.client.post(self.base_url, follow=True)
        content = response.content.decode("utf-8")

        msg = (
            'Este produto possui movimentações, '
            'por isso não pode ser deletado.'
        )

        self.assertIn(msg, content)
        self.assertRedirects(
            response=response,
            expected_url=reverse('products:details', args=(1,)),
            status_code=302,
        )
