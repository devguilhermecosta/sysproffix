from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    AbstractUser,
)
from hospital.models import Hospital


class CustomUserManager(BaseUserManager):
    def create_user(self, f_name, l_name, email, password: str | None = None) -> AbstractUser:  # noqa: E501
        """
            Creates and saves a common user.
        """
        user = self.model(
            first_name=f_name,
            last_name=l_name,
            email=self.normalize_email(email),
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, f_name, l_name, email, password: str | None = None) -> AbstractUser:  # noqa: E501)
        """
            Creates and saves a superuser (programmer user).
        """
        user = self.create_user(f_name, l_name, email, password)
        user.is_admin = True  # type: ignore
        user.is_staff = True
        user.is_hospital_user = True  # type: ignore
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50,
                                  blank=True,
                                  null=False,
                                  verbose_name='Nome',
                                  )
    last_name = models.CharField(max_length=50,
                                 blank=True,
                                 null=False,
                                 verbose_name='sobrenome',
                                 )
    email = models.EmailField(max_length=255,
                              blank=True,
                              null=False,
                              unique=True,
                              error_messages={
                                  'unique': 'e-mail já cadastrado',
                              }
                              )
    is_hospital_user = models.BooleanField(default=True,
                                           verbose_name='usuário de hospital')
    is_admin = models.BooleanField(default=False, verbose_name='administrador')
    is_staff = models.BooleanField(default=False, verbose_name='desenvolvedor')
    created_at = models.DateField(auto_now_add=True, verbose_name='desde')
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
