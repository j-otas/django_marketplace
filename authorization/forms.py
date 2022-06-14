from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from account.models import Account

User = get_user_model()

class AuthUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form_input'
                field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
                field.help_text = ''

        def confirm_login_allowed(self, user):
            if not user.is_active:
                raise forms.ValidationError(
                    _("Your account has expired. \
                            Please click the renew subscription link below"),
                    code='inactive',
                )
