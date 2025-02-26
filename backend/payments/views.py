import json
import logging
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings

from .models import Order, Recipient
from products.models import Product

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            line_items = []
            total_amount = 0
            items_list = []

            for item in data.get('products', []):
                unit_amount = int(item.get('price', 0))
                quantity = int(item.get('quantity', 1))
                total_amount += unit_amount * quantity

                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.get('name', 'Unknown')},
                        'unit_amount': unit_amount,
                    },
                    'quantity': quantity,
                })

                items_list.append({
                    'product_id': item.get('id'),
                    'name': item.get('name', 'Unknown'),
                    'price': item.get('price'),
                    'quantity': quantity,
                })

            success_url = request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}"
            cancel_url = request.build_absolute_uri(reverse('cancel'))

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )

            recipient_data = data.get('recipient')
            if not recipient_data:
                return JsonResponse({'error': 'Missing recipient data'}, status=400)

            recipient = Recipient.objects.create(
                first_name=recipient_data.get('firstName', ''),
                last_name=recipient_data.get('lastName', ''),
                phone=recipient_data.get('phone', ''),
                country=recipient_data.get('country', ''),
                city=recipient_data.get('city', ''),
                street=recipient_data.get('street', ''),
                house=recipient_data.get('house', ''),
                email=recipient_data.get('email', ''),
            )

            order = Order.objects.create(
                recipient=recipient,
                amount=total_amount / 100,  # Convert from cents to dollars
                currency="usd",
                is_paid=False,
                stripe_session_id=session.id,
                items=items_list
            )

            return JsonResponse({'url': session.url})
        except Exception as e:
            logger.exception("Error creating payment session")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def success_view(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return JsonResponse({"error": "session_id is missing"}, status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        logger.exception("Error retrieving Stripe session")
        return JsonResponse({"error": "Payment verification error"}, status=400)

    if session.payment_status != "paid":
        return JsonResponse({"error": "Payment not completed"}, status=400)

    order = get_object_or_404(Order, stripe_session_id=session_id)

    if not order.is_paid:
        # Removing purchased product from the database
        for item in order.items:
            try:
                product_id = item.get('product_id')
                product = Product.objects.get(id=product_id)
                quantity = int(item.get('quantity', 0))
                if product.stock >= quantity:
                    product.stock -= quantity
                else:
                    logger.error(f"Not enough stock for product {product.name} (id: {product_id})")
                    product.stock = 0
                product.save()
            except Product.DoesNotExist:
                logger.error(f"Product with id {item.get('product_id')} not found")

        # Update order status to paid
        order.is_paid = True
        order.save()

    return redirect(settings.FRONTEND_URL)

def cancel_view(request):
    return JsonResponse({"message": "Payment cancelled"}, status=200)
