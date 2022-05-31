import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic import ListView
from .models import Product, SubCategory, MainCategory,FavoriteProduct
from .forms import ProductForm
from django.utils import timezone
from django.template.defaulttags import register
from django import template
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound

register = template.Library()
categories = SubCategory.objects.all()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def product_list(request):
    context = {}
    s_products = {}
    besplatno = []

    products = Product.objects.filter(published_date__lte=timezone.now(), is_active = True).order_by("-published_date", ).order_by("category")
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
    return render(request, 'main_marketplace/product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    is_fav = False
    fav = False
    try:
        if request.user.is_authenticated :
            fav = FavoriteProduct.objects.get(user=request.user, product=product)
    except FavoriteProduct.DoesNotExist:
        fav = False
    if fav:
        is_fav = True
    return render(request, 'main_marketplace/product_detail.html', {'product': product,'categories': categories, 'is_fav':is_fav})

def add_favorite_product(request,pk):

    if is_ajax(request):
        product = Product.objects.get(pk=pk)
        favorite = FavoriteProduct(user=request.user, product=product)
        favorite.save()
        context = {}
        context['is_fav'] = True
        context['product'] = product
        result = render_to_string('main_marketplace/includes/product_detail_favorite.html', context)
        return JsonResponse({'result': result})

def delete_favorite_product(request,pk):
    if is_ajax(request):
        print("ajax получен")
        try:
            product = Product.objects.get(pk=pk)
            favorite = FavoriteProduct.objects.get(user=request.user, product=product)
            favorite.delete()
            context = {}
            context['is_fav'] = False
            context['product'] = product
            result = render_to_string('main_marketplace/includes/product_detail_favorite.html', context)
            return JsonResponse({'result': result})
        except Product.DoesNotExist:
            return HttpResponseNotFound("<h2>Favorite not found</h2>")

def product_create(request):
    if not request.user.is_authenticated:
        return redirect('main_marketplace:product_list')
    context = {}
    create_form = ProductForm()

    if request.method == "GET":
        context['form'] = create_form
        return render(request, 'main_marketplace/product_new.html', context)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            print(request.FILES['image'])
            product.author = request.user
            product.published_date = timezone.now()
            product.save()
            return redirect("main_marketplace:product_detail", product_id = product.id)

    return render(request, 'main_marketplace/product_new.html', context)

def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)
        product = form.save(commit=False)
        product.is_active = False
        product.save()
        return render(request, 'main_marketplace/product_detail.html', {'product': product,'categories': categories})
    except Product.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

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
    return render(request, 'main_marketplace/product_edit.html', {'form': form, 'product_id':product.id})

class FavoriteProductsList(ListView):
    model = FavoriteProduct
    template_name = 'main_marketplace/favorite_products_list.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'favorites': FavoriteProduct.objects.filter(user=self.request.user)}
        temp = FavoriteProduct.objects.filter(user=self.request.user)
        return data

def delete_from_favorit_list(request,pk):
    if is_ajax(request):
        try:
            product = Product.objects.get(pk=pk)
            context = {}

            favorite = FavoriteProduct.objects.get(user=request.user, product=product)
            print("Удалить ",pk)
            favorite.delete()

            context['favorites'] = FavoriteProduct.objects.filter(user=request.user)

            result = render_to_string('main_marketplace/includes/favorite_list_inc.html', context)
            return JsonResponse({'result': result})
        except Product.DoesNotExist:
            return HttpResponseNotFound("<h2>Favorite not found</h2>")
