import json
import logging
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings

from .models import Order, Recipient
from products.models import Product

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        data = json.loads(request.body)
        product_data = data.get('products', [])
        recipient_data = data.get('recipient')

        if not product_data or not recipient_data:
            return JsonResponse({'error': 'Missing data'}, status=400)

        line_items = []
        total_amount = 0
        items_list = []

        for item in product_data:
            product_id = item.get('id')
            quantity = int(item.get('quantity', 1))

            product = Product.objects.get(id=product_id)

            if not product.stripe_price_id:
                return JsonResponse({'error': f"Product {product.name} has no Stripe price ID"}, status=400)

            line_items.append({
                'price': product.stripe_price_id,
                'quantity': quantity
            })

            total_amount += int(product.price * 100) * quantity  # price is Decimal
            items_list.append({
                'product_id': product.id,
                'name': product.name,
                'price': float(product.price),
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
            amount=total_amount / 100,
            currency="usd",
            is_paid=False,
            stripe_session_id=session.id,
            items=items_list
        )

        return JsonResponse({'url': session.url})
    
    except Product.DoesNotExist:
        return JsonResponse({'error': 'One or more products not found'}, status=404)
    except Exception as e:
        logger.exception("Error creating payment session")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id')

        try:
            order = Order.objects.get(stripe_session_id=session_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if not order.is_paid:
            for item in order.items:
                try:
                    product = Product.objects.get(id=item['product_id'])
                    quantity = int(item.get('quantity', 0))
                    product.stock = max(0, product.stock - quantity)
                    product.save()
                except Product.DoesNotExist:
                    continue

            order.is_paid = True
            order.save()

    return JsonResponse({'status': 'success'})
@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id')

        try:
            order = Order.objects.get(stripe_session_id=session_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        if not order.is_paid:
            for item in order.items:
                try:
                    product = Product.objects.get(id=item['product_id'])
                    quantity = int(item.get('quantity', 0))
                    product.stock = max(0, product.stock - quantity)
                    product.save()
                except Product.DoesNotExist:
                    continue

            order.is_paid = True
            order.save()

    return JsonResponse({'status': 'success'})

def success_view(request):
    return redirect(settings.FRONTEND_URL)

def cancel_view(request):
    return JsonResponse({"message": "Payment cancelled"}, status=200)
