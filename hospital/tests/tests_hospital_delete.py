from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.hospital import create_hospital
from hospital.models import Hospital
from django.urls import reverse


class HospitalDeleteTests(TestCaseWithLogin):
    base_url = reverse('hospital:delete', args=(1,))

    def test_the_user_must_be_authenticated(self) -> None:
        """
            to access this page, the user must be authenticated
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/hospitais/1/delete/',
            status_code=302,
        )

    def test_the_user_must_be_an_administrator(self) -> None:
        """
            if the user is not an administrator, he will
            receive a status code 302 (Forbiden).
            the user admin has permission to show the delete
            button, but has not permission to delete.
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()
        response = self.client.post(self.base_url)
        self.assertEqual(response.status_code, 403)

    def test_should_returns_status_code_404(self) -> None:
        """
            if the hospital not exists, the user must receive
            a status code 404.
        """
        self.make_login()
        response = self.client.post(self.base_url)
        self.assertEqual(response.status_code, 404)

    def test_should_render_error_message_if_not_staff(self) -> None:
        """
            if the user is not a staff, an error message must be
            displayed.
        """
        create_hospital()

        user, _ = self.make_login()
        user.is_staff = False
        user.save()

        response = self.client.post(self.base_url, follow=True)
        content = response.content.decode("utf-8")

        self.assertIn(
            'Você não tem permissão para executar esta operação.',
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url='/hospitais/1/details/',
            status_code=302,
        )

    def test_should_detele_the_hospital(self) -> None:
        """
            if the user is a staff, the hospital must be deleted.
        """
        create_hospital()
        self.make_login()

        response = self.client.post(self.base_url, follow=True)
        content = response.content.decode("utf-8")

        self.assertFalse(Hospital.objects.exists())
        self.assertIn(
            'Registro deletado com sucesso',
            content,
        )
        self.assertRedirects(
            response=response,
            expected_url='/hospitais/list/',
            status_code=302,
        )
