import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from .models import Product, SubCategory, MainCategory
from .forms import ProductForm
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

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    is_fav = False
    fav = False
    # try:
    #     if request.user.is_authenticated :
    #         fav = FavoriteProduct.objects.get(user=request.user, product=product)
    # except FavoriteProduct.DoesNotExist:
    #     fav = False
    # if fav:
    #     is_fav = True
    return render(request, 'product_detail.html', {'product': product,'categories': categories, 'is_fav':is_fav})

def product_create(request):
    if not request.user.is_authenticated:
        return redirect('main_marketplace:product_list')
    context = {}
    create_form = ProductForm()

    if request.method == "GET":
        context['form'] = create_form
        return render(request, 'product_new.html', context)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            print(request.FILES['image'])
            product.author = request.user
            product.published_date = timezone.now()
            product.save()
            return redirect("main_marketplace:product_detail", product_id = product.id)

    return render(request, 'product_new.html', context)

def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.published_date = timezone.now()
            product.save()
            return redirect('main_marketplace:product_detail', product_id=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_edit.html', {'form': form, 'product_id':product.id})
