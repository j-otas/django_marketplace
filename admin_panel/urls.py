from django.urls import path
from . import views


app_name = "admin_panel"

urlpatterns = [
    path('', views.main_admin_panel, name='admin_main'),
    path('tables/<int:pk>/', views.admin_current_table, name='admin_current_table'),

    path('accept_data', views.accept_change_data, name='accept_data'),
    path('add_modal_form', views.add_modal_form, name='add_modal_form'),

    path('accept_add_data', views.accept_add_data, name='accept_add_data'),
    path('delete_object', views.delete_object, name='delete_object'),

    path('moderate/products', views.ModerateProductList.as_view(), name='moderate_product'),
    path('moderate/products/accept/<int:pk>', views.accept_moderate_product, name='accept_moderate_product'),
    path('moderate/products/cancel/<int:pk>', views.cancel_moderate_product, name='cancel_moderate_product'),

    path('moderate/users', views.ModerateUserList.as_view(), name='moderate_user'),
    path('moderate/users/accept/<int:pk>', views.accept_moderate_user, name='accept_moderate_user'),
    path('moderate/users/cancel/<int:pk>', views.cancel_moderate_user, name='cancel_moderate_user'),

]