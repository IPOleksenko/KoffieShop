from django.contrib import admin
from django.urls import path
from products.views import ProductListView, ProductDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/products/', ProductListView.as_view(), name='product_list'),
    path('api/products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
]
