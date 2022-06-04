from django.urls import path
from . import views

app_name = "main_marketplace"

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('select/city/<int:city_id>/', views.select_city, name='select_city'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:product_id>/edit', views.product_edit, name='product_edit'),
    path('search', views.search_results_list, name='search_results'),
    path('favorite', views.FavoriteProductsList.as_view(), name='favorite_products'),
    path('product/<int:pk>/favorite_add', views.add_favorite_product, name='add_favorite_product'),
    path('product/<int:pk>/favorite_delete', views.delete_favorite_product, name='delete_favorite_product'),
    path('product/<int:pk>/favorite_list_delete', views.delete_from_favorit_list, name='delete_from_favorit_list'),

]