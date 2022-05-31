from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 60, help_text = "Рекуайред. Add a valid email add")
    cellphone = PhoneNumberField()
    class Meta:
        model = Account
        fields = ("email", "first_name", "city", "cellphone", "password1", "password2")
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_input'
            if field_name == 'password1' or field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Пароль'
            else:
                field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ''