from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import base64
from django.core.files.base import ContentFile

from messengerapp.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id
        self.user_id = self.scope['user'].id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'read_message',
                'chat_id': self.chat_id,
                'user_id': self.user_id
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'message':
            author_id = text_data_json['author_id']
            author_name = text_data_json['author_name']
            author_img = text_data_json['author_img']
            message = text_data_json['message']
            time = text_data_json['time']
            members = text_data_json['members']
            image_data = text_data_json['image']

            if image_data:
                img_format, img_str = image_data.split(';base64,')
                ext = img_format.split('/')[-1]
                img_file = ContentFile(
                    base64.b64decode(img_str),
                    name=f'chat_{self.chat_id}_user_{author_id}_at_{time}.' + ext
                )

                Message.objects.create(chat_id=self.chat_id, author_id=author_id, message=message, image=img_file)
            else:
                Message.objects.create(chat_id=self.chat_id, author_id=author_id, message=message)

            # send message
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'author_id': author_id,
                    'author_name': author_name,
                    'author_img': author_img,
                    'message': message,
                    'members': members,
                    'time': time,
                    'image': image_data
                }
            )
        elif action == 'read':
            chat_id = text_data_json['chat_id']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'read_message',
                    'chat_id': chat_id,
                    'user_id': self.user_id
                }
            )

    def send_message(self, event):
        self.send(text_data=json.dumps({
            'event': "new_msg",
            'message': event['message'],
            'author_id': event['author_id'],
            'author_name': event['author_name'],
            'author_img': event['author_img'],
            'time': event['time'],
            'image': event['image']
        }))

        for receiver_id in eval(event['members']):
            if receiver_id == self.user_id:
                continue

            # send notifications
            async_to_sync(self.channel_layer.group_send)(
                f'user_{receiver_id}',
                {
                    'type': 'notice.send',
                    'obj': "message",
                    'chat_id': self.chat_id
                }
            )

    def read_message(self, event):
        Message.objects.filter(chat_id=event['chat_id']).filter(is_read=False).exclude(
            author_id=event['user_id']).update(is_read=True)

        self.send(text_data=json.dumps({
            'event': "read",
            'chat_id': event['chat_id'],
            'user_id': str(event['user_id'])
        }))


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = 'user_%s' % self.user_id

        print(f'connect user to group {self.group_name}')

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def notice_send(self, event):
        self.send(text_data=json.dumps({
            'event': "notice",
            'obj': event['obj'],
            'chat_id': str(event['chat_id'])
        }))