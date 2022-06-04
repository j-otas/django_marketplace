from .forms import AuthUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import login

class MyProjectLogout(LogoutView):
    next_page=None

    success_url = reverse_lazy('main_marketplace:product_list')

class AuthUserView(LoginView):
    template_name = 'authorization/auth.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main_marketplace:product_list')

    def form_valid(self, form):
        del self.request.session["selected_city_id"]
        return super(AuthUserView, self).form_valid(form)
