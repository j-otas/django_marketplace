from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from account.forms import RegistrationForm
from django.urls import reverse, reverse_lazy
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            new_account = form.save(commit=False)
            new_account.set_password(raw_password)
            new_account.save()

            login(request, new_account)
            print("Регистрация успешна")
            return redirect('main_marketplace:product_list')
        else:
            print("Регистрация НЕуспешна")
            context["form"] = form
            return render(request, 'authorization/reg.html', context)
    else: #GET request
        form = RegistrationForm()
        context['form'] = form
        return render(request, 'authorization/reg.html', context)