from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.auth.user import create_superuser
from django.urls import reverse
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserDeleteTests(TestCaseWithLogin):
    base_url = reverse('users:delete', args=(1,))

    def setUp(self, *args, **kwargs) -> None:
        create_superuser('maria', 'da silva', 'maria@email.com', '123456')
        return super().setUp(*args, **kwargs)

    def test_user_must_be_loged_in(self) -> None:
        """
            if the uer is not authenticated, will be redirected
            to login page.
        """
        response = self.client.post(self.base_url)

        self.assertRedirects(
            response=response,
            expected_url='/?next=/usuarios/1/delete/',
            status_code=302,
        )

    def test_user_should_return_404_if_user_not_found(self) -> None:
        self.make_login()
        response = self.client.post(reverse('users:details', args=(10,)))
        self.assertEqual(response.status_code, 404)

    def test_should_show_permission_denied_if_the_user_is_not_admin(self) -> None:  # noqa: E501
        """
            to access the view the user must be an administrator
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.post(self.base_url)

        self.assertEqual(response.status_code, 403)

    def test_should_delete_the_user(self) -> None:  # noqa: E501
        self.make_login()

        response = self.client.post(self.base_url, follow=True)

        self.assertIn(
            'Usuário deletado com sucesso',
            response.content.decode("utf-8"),
        )
        self.assertRedirects(
            response=response,
            expected_url='/usuarios/list/',
            status_code=302,
        )
