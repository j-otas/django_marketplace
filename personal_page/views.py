from django.views.generic.base import View
from django.shortcuts import render
from main_marketplace.models import Product, SubCategory, MainCategory,FavoriteProduct
from account.models import Account
categories = SubCategory.objects.all()

class Personal (View):
    def get(self, request, *args, **kwargs):
        account_pk = self.kwargs['user_id']
        user = self.request.user
        if user.is_authenticated:
            cur_user = user
        cur_user = Account.objects.get(pk=account_pk)
        # if cur_user:
        user_active_products = Product.objects.filter(author=cur_user, is_active = True)
        user_unactive_products = Product.objects.filter(author=cur_user, is_active = False)
        return render(self.request, 'personal_page/personal_page.html', {'cur_user': cur_user,
                                                                         'user_active_products': user_active_products,
                                                                         'user_unactive_products': user_unactive_products,
                                                                         'categories': categories})
