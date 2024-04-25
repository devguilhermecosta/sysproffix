from .. regex import strong_password
from django.test import TestCase


class StrongPasswodTests(TestCase):
    def test_should_return_false(self) -> None:
        """
            it should return False if the password
            not match.
        """
        password_match = strong_password('123abc')
        self.assertFalse(password_match)

    def test_should_return_true(self) -> None:
        """
            it should return True if the password match.
        """
        password_match = strong_password('Abc123@@')
        self.assertTrue(password_match)
