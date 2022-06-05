import os
from django.db import models
from django.conf import settings
from django.dispatch import receiver
import json
class MainCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Главная категория'
        verbose_name_plural = 'Главные категории'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    main_category =  models.ForeignKey(MainCategory, related_name = 'main_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name = 'city', verbose_name = "Город", on_delete = models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Название")

    category = models.ForeignKey(SubCategory, related_name = "products", on_delete = models.CASCADE)
    main_category = models.ForeignKey(MainCategory, related_name = 'main_category_product', on_delete=models.CASCADE, default = None, null = True, blank = True)
    address = models.CharField(max_length=200, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")
    published_date = models.DateTimeField(blank=True, null=True)
    cost = models.fields.IntegerField(blank=False, null=True, verbose_name="Цена")
    image = models.ImageField(blank=True, null=False, verbose_name="Изображение", upload_to='product_images/', default='product_images/no_image_product.jpg')
    is_active = models.BooleanField(default = False)
    is_moderated = models.BooleanField(default = False)



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.category.main_category.name +"-"+self.title

    def save(self, *args, **kwargs):
        print("ФУНКЦИЯ СОЗДАНИЯЯЯ")
        self.main_category = self.category.main_category
        super(Product, self).save(*args, **kwargs)

    @classmethod
    def create(new_product):
        print("ФУНКЦИЯ СОЗДАНИЯЯЯ")
        book = new_product(main_category = new_product.category.main_category)
        return book
    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     super(Product, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт(товар)'
        verbose_name_plural = 'Продукты(товары)'

class FavoriteProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.product) +'-'+str(self.user)
    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'

@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаление изображений из файловой системы
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Удаление старых изображений из файловой системы при обновлении
    """
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image
        if not old_file:
            return False
    except Product.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

