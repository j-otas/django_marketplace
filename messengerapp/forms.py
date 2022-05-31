from itertools import chain
from django import forms
from django.core.files.images import get_image_dimensions
from django.db.models import QuerySet
from django.forms import ModelForm

from account.models import Account
from messengerapp.models import Message, Chat


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}


class CreateChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = ("title", "image", "members", "type")

    def __init__(self, *args, **kwargs):
        super(CreateChatForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'b-form__input'
            field.widget.attrs["placeholder"] = self.Meta.model._meta.get_field(field_name).verbose_name.capitalize
            field.help_text = ""

            if field_name == 'members':
                field.label = 'Участники (Выберите с зажатым Ctrl)'

    def clean_members(self):
        user_qset = Account.objects.filter(pk=self.data['user_id'])
        members = self.cleaned_data['members']

        if not user_qset[0] in members:
            members = list(chain(members, user_qset))
        return members

    def clean_image(self):
        image = self.cleaned_data['image']

        if not image:
            return False

        try:
            w, h = get_image_dimensions(image)

            max_width = max_height = 1920
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    f'Пожалуйста, испльзуйте изображения {max_width} x {max_height} пикселов или меньше.')

            main, sub = image.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError('Пожалуйста, используйте JPEG, GIF или PNG изображения.')

            if len(image) > (2048 * 1024):
                raise forms.ValidationError('Размер файла не может превышать 2 Мб.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            return image

        except TypeError:
            raise forms.ValidationError('Пожалуйста, используйте JPEG, GIF или PNG изображения.')

        return image