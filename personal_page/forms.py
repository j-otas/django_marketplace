from django import forms
from account.models import Account



class PersonalEditForm(forms.ModelForm):
    hide_cellphone = forms.BooleanField(required=False)
    avatar = forms.ImageField(label= 'Аватар',required=False, error_messages = {'invalid': "Только изображения"}, widget=forms.FileInput)
    class Meta:
        model = Account
        fields = ("email", "first_name", "last_name", "city", "cellphone", "avatar", "hide_cellphone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form_input'
            field.widget.attrs['placeholder'] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ''
