import stripe
from django.conf import settings
from django.contrib import admin
from .models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ("id", "name", "price", "stock")
    search_fields = ("name",)
    list_filter  = ("price", "stock")
    ordering      = ("id",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and not obj.stripe_product_id:
            stripe_prod = stripe.Product.create(
                name=obj.name,
                metadata={"django_id": obj.id}
            )
            stripe_price = stripe.Price.create(
                product=stripe_prod.id,
                unit_amount=int(obj.price * 100),
                currency="usd",
            )
            obj.stripe_product_id = stripe_prod.id
            obj.stripe_price_id   = stripe_price.id
            obj.save(update_fields=["stripe_product_id", "stripe_price_id"])
