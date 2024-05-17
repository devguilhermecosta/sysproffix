from django.urls import reverse
from parameterized import parameterized  # type: ignore
from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.product import create_product_group


class ProductGroupListTests(TestCaseWithLogin):
    base_url = reverse('products:group_list')

    def test_the_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/products/groups/',
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

    def test_should_render_all_registered_gropus(self) -> None:
        self.make_login()

        for i in range(3):
            create_product_group(name=f'group-{i}')

        response = self.client.get(self.base_url)

        self.assertEqual(len(response.context['groups']), 3)
        self.assertIn(
            'Group-1',
            response.content.decode("utf-8")
        )

    @parameterized.expand([
        'Grupos',
        'nome',
        'Group-0',
        'Group-1',
        'Group-2',
        'novo',
        'href="/products/groups/register/"'
    ])
    def test_should_render_the_correct_content(self, txt: str) -> None:
        self.make_login()

        for i in range(3):
            create_product_group(name=f'group-{i}')

        response = self.client.get(self.base_url)

        self.assertIn(
            txt,
            response.content.decode("utf-8")
        )
