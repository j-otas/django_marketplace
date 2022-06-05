from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from account.models import Account
from main_marketplace.models import Product


class ChatManager(models.Manager):
    use_for_related_fields = True

    def unreaded(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_read=False)
        return qs.exclude(last_message__author=user) if user else qs


class Chat(models.Model):
    product = models.ForeignKey(Product, verbose_name="Обсуждаемый товар", on_delete=models.CASCADE, default = 0)
    members = models.ManyToManyField(Account, verbose_name="Участник", blank=False)
    title = models.CharField(max_length=50, blank=False, verbose_name='Название')
    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    objects = ChatManager()

    class Meta:
        verbose_name = 'Чаты'
        verbose_name_plural = 'Чаты'
        ordering = ('-last_message',)

    @property
    def get_members(self):
        qs = [user.id for user in self.members.all()]
        print(qs)
        return qs

    def __str__(self):
        return f'{self.members.all()}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE)
    author = models.ForeignKey(Account, verbose_name="Пользователь", on_delete=models.DO_NOTHING)
    message = models.TextField("Сообщение")
    pub_date = models.DateTimeField('Дата сообщения', default=timezone.now)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.message


@receiver(post_save, sender=Message)
def post_save_comment(sender, instance, created, **kwargs):
    if created:
        instance.chat.last_message = instance
        instance.chat.save(update_fields=['last_message'])