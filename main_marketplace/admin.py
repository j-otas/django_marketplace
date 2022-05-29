from django.contrib import admin

# Register your models here.
from .models import City, MainCategory, SubCategory, Product

admin.site.register(City)
admin.site.register(SubCategory)
admin.site.register(MainCategory)
admin.site.register(Product)
