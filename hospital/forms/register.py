from django import forms
from hospital.models import Hospital
from utils.strings import normalize
from utils.forms import required_field


class HospitalRegisterForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = [
            'name',
            'city',
            'state'
        ]

    def clean_name(self):
        name = required_field(self.cleaned_data["name"])
        return normalize(name)

    def clean_city(self):
        city = required_field(self.cleaned_data["city"])
        return normalize(city)

    def clean_state(self):
        state = required_field(self.cleaned_data["state"])
        return normalize(state)
