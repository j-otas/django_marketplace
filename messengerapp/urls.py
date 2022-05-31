from django.urls import path
import messengerapp.views as messengerapp

app_name = 'messenger'

urlpatterns = [
    path('', messengerapp.DialogsView.as_view(), name='dialogs'),
    path('create/<friend_id>/', messengerapp.create_dialog, name='create_dialog'),
    path('create_chat/', messengerapp.CreateChatView.as_view(), name='create_chat'),
    path('delete/<chat_id>/', messengerapp.delete_dialog, name='delete_chat'),
    path('edit/<pk>/', messengerapp.EditChatView.as_view(), name='edit_chat'),
    path('<chat_id>/', messengerapp.MessagesView.as_view(), name='messages'),

    path('get_messages/<chat_id>/', messengerapp.get_messages, name='get_messages'),
    path('get/new_mes_count/', messengerapp.get_new_mes_count, name='get_new_mes_count'),
    path('get/update_dialogs/', messengerapp.update_chats_list, name='update_dialogs'),
]