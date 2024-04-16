from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):
    base_url = '/'

    def test_home_url_is_correct(self) -> None:
        url = reverse('home:login')

        self.assertEqual(url, self.base_url)
