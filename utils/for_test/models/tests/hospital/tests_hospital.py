from django.test import TestCase
from ...hospital import create_hospital
from hospital.models import Hospital


class HospitalTests(TestCase):
    def test_should_return_an_instance_of_hospital(self) -> None:
        hospital = create_hospital(name='Hospital Health')
        self.assertTrue(isinstance(hospital, Hospital))
