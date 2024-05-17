from django.urls import reverse
from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.product import create_product_group, create_product


class ProductGroupDeleteTests(TestCaseWithLogin):
    base_url = reverse('products:group_delete', args=(1,))

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.post(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/groups/1/delete/',
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

    def test_should_return_404_if_the_group_dont_exists(self) -> None:
        self.make_login()
        response = self.client.post(self.base_url)
        self.assertEqual(response.status_code, 404)

    def test_should_not_delete_the_group_if_it_has_products(self) -> None:
        self.make_login()
        create_product()  # creates the product and group
        response = self.client.post(self.base_url, follow=True)
        content = response.content.decode("utf-8")

        self.assertIn(
            'Você não pode deletar este grupo, pois existem '
            'produtos ativos e vinculados a ele',
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('products:group_list'),
            status_code=302,
        )

    def test_should_delete_the_group(self) -> None:
        self.make_login()
        create_product_group()
        response = self.client.post(self.base_url, follow=True)
        content = response.content.decode("utf-8")

        self.assertIn(
            'Grupo deletado com sucesso',
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url=reverse('products:group_list'),
            status_code=302,
        )
