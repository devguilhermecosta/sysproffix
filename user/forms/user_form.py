from django import forms
from django.contrib.auth import get_user_model


class UserRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field[0])

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            'is_hospital_user',
            'is_admin',
            'is_staff',
            'hospital',
        ]

        labels = {
            "first_name": "nome",
            "last_name": "sobrenome",
            "email": "email",
            "is_hospital_user": "usuário de hospital",
            "is_admin": "administrador",
            "is_staff": "desenvolvedor",
            "hospital": "instituição",
        }

        widgets = {
            "is_hospital_user": forms.CheckboxInput(
                attrs={
                    "disabled": True,
                }),
        }

# uma senha temporária será criada.
# user.is_active = True é padrão?
