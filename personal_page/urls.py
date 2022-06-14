from django.urls import path
from . import views

app_name = 'personal_page'

urlpatterns = [
    path('<int:user_id>/', views.Personal.as_view(), name='personal_page'),
    path('<int:user_id>/edit', views.personal_edit, name='personal_edit'),
    path('delete/<int:user_id>', views.delete_profile, name='delete_profile'),
]