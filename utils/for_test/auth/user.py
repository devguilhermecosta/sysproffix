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
