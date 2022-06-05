# Generated by Django 4.0.4 on 2022-06-04 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_account_hide_cellphone_account_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, default='users_avatars/default.png', null=True, upload_to='user_images', verbose_name='Аватар пользователя'),
        ),
    ]