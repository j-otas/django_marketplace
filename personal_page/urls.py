from django.urls import path
from . import views

app_name = 'personal_page'

urlpatterns = [
    path('<int:user_id>/', views.Personal.as_view(), name='personal_page'),
]