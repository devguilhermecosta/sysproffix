from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ResetPasswordForm(forms.Form):
    email = forms.CharField(
        required=False,
        label='e-mail',
        help_text=(
            'Informe seu e-mail de cadastro.\n'
            'Você receberá via e-mail uma senha temporária de acesso.'
        ),
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Digite seu email...',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        UserModel = get_user_model()

        if not email:
            raise ValidationError(
                'Campo obrigatório',
                code='required',
            )

        user = UserModel.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                'Usuário não cadastrado',
                code='invalid',
            )

        return email
