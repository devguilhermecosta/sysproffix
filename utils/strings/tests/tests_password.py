from django.test import TestCase
from .. password import generate_password


class PasswordGenerateTests(TestCase):
    def test_must_return_a_string(self) -> None:
        password = generate_password()
        self.assertTrue(isinstance(password, str))

    def test_password_must_have_correct_length(self) -> None:
        password = generate_password()
        self.assertTrue(len(password) >= 8 and len(password) <= 16)
