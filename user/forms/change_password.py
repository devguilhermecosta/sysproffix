from typing import Any
from django import forms
from utils.strings.regex import strong_password


help_text = (
    'A senha precisa ter pelo menos:\n'
    '- oito catacteres\n'
    '- uma letra maíuscula\n'
    '- uma letra minúscula\n'
    '- um número.'
)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='nova senha',
                               required=False,
                               help_text=help_text,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': '**********',
                                   }
                               ))
    password_confirm = forms.CharField(label='repita a senha',
                                       required=False,
                                       widget=forms.PasswordInput(
                                           attrs={
                                               'placeholder': '**********',
                                           }
                                       ))

    def clean(self) -> dict[str, Any]:
        data = super().clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if not password:
            self.add_error('password', 'campo obrigatório')

        if not password_confirm:
            self.add_error('password_confirm', 'campo obrigatório')

        if password != password_confirm:
            self.add_error('password', 'as senhas precisam ser iguais')

        if not strong_password(password):  # type: ignore
            self.add_error(
                'password',
                help_text
            )

        return super().clean()
