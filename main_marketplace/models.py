from django.db import models
from django.conf import settings

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

    address = models.CharField(max_length=200, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")
    published_date = models.DateTimeField(blank=True, null=True)
    cost = models.fields.IntegerField(blank=False, null=True, verbose_name="Цена")
    image = models.ImageField(blank=True, null=True, verbose_name="Изображение", upload_to='product_images/', default=None)
    is_active = models.BooleanField(default = False)
    is_moderated = models.BooleanField(default = False)



    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.category.main_category.name +"-"+self.title

    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     super(Product, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт(товар)'
        verbose_name_plural = 'Продукты(товары)'

