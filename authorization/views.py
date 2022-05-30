from .forms import AuthUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy

class MyProjectLogout(LogoutView):
    next_page=None
    success_url = reverse_lazy('main_marketplace:product_list')

class AuthUserView(LoginView):
    template_name = 'authorization/auth.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main_marketplace:product_list')