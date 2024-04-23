from django.test import TestCase
from ..normalize import normalize


class NormalizeTests(TestCase):
    def test_must_return_the_value_on_lowercase(self) -> None:
        data = 'ABC'
        data_normalize = normalize(data)
        self.assertEqual(data_normalize, 'abc')
