# Generated by Django 4.0.4 on 2022-05-31 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='product_images/no_image_product.jpg', null=True, upload_to='product_images/', verbose_name='Изображение'),
        ),
    ]
