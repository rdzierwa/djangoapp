# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, add_product, DeleteProductView, WarehouseCreateView
from . import views
router = DefaultRouter()
router.register(r'productapp', ProductViewSet, basename='product')


app_name = 'productapp'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list_products'),
    path('add-warehouse/', WarehouseCreateView.as_view(), name='add_warehouse'),

    path('api/product/add_product/', add_product, name='add_product'),

    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', DeleteProductView.as_view(), name='delete_product'),
    path('api/product/<int:product_id>/synchronize/', views.synchronize_product, name='synchronize_product'),
] + router.urls

