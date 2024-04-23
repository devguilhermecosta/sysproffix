from django.core.exceptions import ValidationError
from django.test import TestCase
from ..clean import required_field


class RequiredFieldTests(TestCase):
    def test_must_return_validation_error_if_not_data(self) -> None:
        with self.assertRaises(ValidationError):
            required_field('')

    def test_must_return_the_same_data(self) -> None:
        """
            if data, the function must return the same data.
        """
        data = required_field('anything')
        self.assertEqual(data, 'anything')
