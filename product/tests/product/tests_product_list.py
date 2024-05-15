from django.urls import reverse
from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models import product


class ProductListTests(TestCaseWithLogin):
    base_url = reverse('products:list')

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/list/',
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

    def test_should_render_all_registered_products(self) -> None:
        self.make_login()

        product.create_product_in_batch(4)
        response = self.client.get(self.base_url)

        self.assertEqual(
            len(response.context['products']),
            4
        )
        self.assertIn(
            'Product-1',
            response.content.decode("utf-8"),
        )

    def test_should_render_the_button_to_add_a_new_product(self) -> None:
        self.make_login()
        response = self.client.get(self.base_url)

        self.assertIn(
            'novo',
            response.content.decode("utf-8"),
        )
        self.assertIn(
            'href="/products/new/"',
            response.content.decode("utf-8"),
        )
