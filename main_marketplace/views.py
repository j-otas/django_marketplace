from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import Product, SubCategory, MainCategory
from django.utils import timezone
from django.template.defaulttags import register
from django import template

register = template.Library()
categories = SubCategory.objects.all()

def product_list(request):
    context = {}
    s_products = {}
    besplatno = []

    products = Product.objects.filter(published_date__lte=timezone.now()).order_by("-published_date", ).order_by("category")
    for product in products:
        if product.cost == 0:
            besplatno.append(product)
        if len(besplatno) == 6 or len(besplatno)>6:
            break
    print(products)

    for product in products:
        if not s_products.get(product.category.main_category.name):
            s_products[product.category.main_category.name] = [product,]
            continue
        s_products[product.category.main_category.name].append(product)
    print(s_products)


    context['products'] = products
    context['categories'] = categories
    context['besplatno'] = besplatno
    context['s_products'] = s_products
    return render(request, 'product_list.html', context)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
