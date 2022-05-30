from django.urls import path
from . import views
# from account.views import registration_view

app_name = 'authorization'

urlpatterns = [
    #path('reg/', registration_view, name='reg_page'),
    path('', views.AuthUserView.as_view(), name='auth_page'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]