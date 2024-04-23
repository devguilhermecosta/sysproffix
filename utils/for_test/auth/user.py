from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


def create_superuser(f_name: str, l_name: str, email: str, password: str) -> AbstractUser:  # noqa: E501
    UserModel = get_user_model()

    user = UserModel.objects.create_superuser(  # type: ignore
        f_name,
        l_name,
        email,
        password,
    )

    return user


def create_users_in_batch(num_of_users) -> list[AbstractUser]:
    list_of_users: list[AbstractUser] = []

    for i in range(num_of_users):
        user = create_superuser(
            f_name=f'first-name-for-user-{i}',
            l_name=f'last-name-for-user-{i}',
            email=f'email-for-user-{i}@email.com',
            password='123456',
        )

        list_of_users.append(user)

    return list_of_users
