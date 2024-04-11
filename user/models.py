from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    AbstractUser,
)
from hospital.models import Hospital


class CustomUserManager(BaseUserManager):
    def __create_user(self, f_name, l_name, email, password: str | None = None) -> AbstractUser:  # noqa: E501
        """
            Creates and saves a common user.
        """
        user = self.model(
            first_name=f_name,
            last_name=l_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_hospital_user(self,
                             f_name,
                             l_name,
                             email,
                             password: str | None = None,
                             hospital: Hospital | None = None) -> AbstractUser:  # noqa: E501
        """
            Creates and saves a hospital user.
        """
        if not hospital:
            raise ValidationError(
                "The user must have an hospital.",
                code='required',
            )
        user = self.__create_user(f_name, l_name, email, password)
        user.hospital = hospital  # type: ignore
        user.is_hospital_user = True  # type: ignore

        return user

    def create_admin_user(self, f_name, l_name, email, password: str | None = None) -> AbstractUser:  # noqa: E501
        """
            Creates and saves a user admin (user who is part of the team).
        """
        user = self.__create_user(f_name, l_name, email, password)
        user.is_admin = True  # type: ignore

        return user

    def create_superuser(self, f_name, l_name, email, password: str | None = None) -> AbstractUser:  # noqa: E501)
        """
            Creates and saves a superuser (programmer user).
        """
        user = self.__create_user(f_name, l_name, email, password)
        user.is_admin = True  # type: ignore
        user.is_staff = True

        return user


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=255,
                              blank=False,
                              null=False,
                              unique=True,
                              verbose_name="email adress",
                              )
    is_hospital_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    hospital = models.ForeignKey(Hospital,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def __str__(self) -> str:
        return self.full_name

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True
