from django.urls import reverse
from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.auth.user import create_users_in_batch
from parameterized import parameterized  # type: ignore
from datetime import date


class UserListsTests(TestCaseWithLogin):
    base_url = reverse('users:list')

    def test_user_must_be_loged_in(self) -> None:
        """
            if the uer is not authenticated, will be redirected
            to login page.
        """
        response = self.client.get(self.base_url)

        self.assertRedirects(
            response=response,
            expected_url='/?next=/usuarios/list/',
            status_code=302,
        )

    def test_must_show_permission_denied_if_the_user_is_not_admin(self) -> None:  # noqa: E501
        """
            to access the view the user must be an administrator
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 403)

    @parameterized.expand([
        'first-name-for-user-0'.title(),
        'first-name-for-user-1'.title(),
        'first-name-for-user-2'.title(),
        'href="/usuarios/1/details/',  # url to user details
        'usuário',  # table header
        'desde',  # table header
        'ativo',  # table header
        'desen.',  # table header
        'hospital',  # table header
        'instituição',  # table header
        date.today().strftime('%d/%m/%Y'),  # table data for 'desde'
    ])
    def test_must_show_all_users(self, text: str) -> None:
        """
            this test checks if the content of the page is correct
        """
        create_users_in_batch(3)
        self.make_login()

        response = self.client.get(self.base_url)

        self.assertIn(text, response.content.decode("utf-8"))

    def test_context_must_have_3_users(self) -> None:
        """
            this test creates 3 users.
            must have 3 users in context['users']
        """
        create_users_in_batch(2)  # create 2 users
        self.make_login()  # create 1 user

        response = self.client.get(self.base_url)

        self.assertEqual(3, len(response.context['users']))
