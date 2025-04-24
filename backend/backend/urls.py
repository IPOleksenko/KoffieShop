from django.contrib import admin
from django.urls import path
from products.views import ProductListView, ProductDetailView
from payments.views import create_checkout_session, stripe_webhook, success_view, cancel_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('api/payment/stripe/webhook/', stripe_webhook, name='stripe-webhook'),

    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
    
    path('api/products/', ProductListView.as_view(), name='product_list'),
    path('api/products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
]
