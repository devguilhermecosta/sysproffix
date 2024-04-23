from utils.for_test.auth.authentication import TestCaseWithLogin
from utils.for_test.models.hospital import create_hospital
from django.urls import reverse


class HospitalListTests(TestCaseWithLogin):
    base_url = reverse('hospital:list')

    def test_user_must_be_logged_in(self) -> None:
        """
            to access this page, the user must be logged in.
        """
        response = self.client.get(self.base_url)
        self.assertRedirects(
            response=response,
            expected_url='/?next=/hospitais/list/',
            status_code=302,
        )

    def test_the_user_must_be_admin(self) -> None:
        """
            to access this page, the user must be an administrator.
        """
        user, _ = self.make_login()
        user.is_admin = False  # type: ignore
        user.save()

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, 403)

    def test_should_render_the_correct_content(self) -> None:
        """
            All registered Hospitals must by displayed.
        """
        self.make_login()

        # creates 3 instances of hospital
        for i in range(3):
            create_hospital(name=f'Hospital-{i}')

        response = self.client.get(self.base_url)
        content = response.content.decode("utf-8")

        self.assertEqual(
            len(response.context['hospitals']),
            3,
        )
        self.assertIn(
            'Hospital-0',
            content,
        )
        self.assertIn(
            'São Paulo',
            content,
        )
        self.assertIn(
            'SP',
            content,
        )
