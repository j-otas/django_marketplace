from django.views.generic.base import View
from django.shortcuts import render
from main_marketplace.models import Product, SubCategory, MainCategory,FavoriteProduct
from account.models import Account
from django.http import HttpResponse
from .forms import PersonalEditForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage



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
                                                                         'user_unactive_products': user_unactive_products,})

def personal_edit(request,user_id):
    cur_user = Account.objects.get(pk=user_id)
    if cur_user.id != user_id:
        return HttpResponse("Нельзя редактировать чужие аккаунты")
    else:
        if request.method == "POST":
            form = PersonalEditForm(request.POST, instance=cur_user)
            if form.is_valid():
                cur_user = form.save(commit=False)
                if request.FILES:
                    fs = FileSystemStorage()
                    avatar_file = fs.save(('users_avatars/' + request.FILES['avatar'].name), request.FILES['avatar'])
                    cur_user.avatar = 'users_avatars/' + str(request.FILES['avatar'])
                else:
                    print(form.instance.avatar)
                    cur_user.avatar = form.instance.avatar
                cur_user.save()
                return redirect('personal_page:personal_page', user_id=cur_user.pk)
        if request.method == "GET":
            form = PersonalEditForm(instance=cur_user)
            print("OOOU - ", form.instance.avatar)
        return render(request, 'personal_page/personal_edit.html',
                      {'form': form, })