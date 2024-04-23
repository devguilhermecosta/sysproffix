from django.test import TestCase
from django.contrib.auth import get_user_model
from utils.for_test.auth.user import (
    create_superuser,
    create_users_in_batch
)


UserModel = get_user_model()


# this class must test the utils/fot_test/auth/user.py file
class UserTests(TestCase):
    def test_create_superuser_func_should_create_a_new_superuser(self) -> None:
        user = create_superuser('jhon', 'doe', 'j@email.com', '123')
        self.assertTrue(isinstance(user, UserModel))

    def test_create_users_in_batch_must_create_severals_users(self) -> None:
        """
            this function must create an X amount
            of users according to the input.
        """
        user_list = create_users_in_batch(3)
        self.assertTrue(isinstance(user_list[0], UserModel))
        self.assertEqual(len(user_list), 3)
