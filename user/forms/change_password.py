from django import forms


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='nova senha',
                               widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': '**********',
                                   }
                               ))
    password_confirm = forms.CharField(label='repita a senha',
                                       widget=forms.PasswordInput(
                                           attrs={
                                               'placeholder': '**********',
                                           }
                                       ))


# TODO continuar daqui
