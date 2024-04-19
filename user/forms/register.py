from django import forms
from django.contrib.auth import get_user_model
from utils.forms import required_field
from utils.strings import normalize


class UserRegisterForm(forms.ModelForm):

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

    def clean_first_name(self):
        first_name = required_field(self.cleaned_data["first_name"])
        return normalize(first_name)

    def clean_last_name(self):
        last_name = required_field(self.cleaned_data["last_name"])
        return normalize(last_name)

    def clean_email(self):
        email = required_field(self.cleaned_data["email"])
        return email  # the Model makes the normalize process

    def clean_hospital(self):
        hospital = required_field(self.cleaned_data["hospital"])
        return hospital
