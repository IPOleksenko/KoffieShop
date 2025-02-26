import json
import logging
import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from .models import Order, Recipient

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
                    'name': item.get('name', 'Unknown'),
                    'price': item.get('price'),
                    'quantity': quantity
                })

            # Generating absolute URLs using route names from urls.py
            success_url = request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}"
            cancel_url = request.build_absolute_uri(reverse('success'))

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )

            # Processing recipient data
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
    # Extract session_id from GET parameters
    session_id = request.GET.get("session_id")
    if not session_id:
        return JsonResponse({"error": "session_id is missing"}, status=400)

    try:
        # Retrieve session data from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        logger.exception("Error retrieving Stripe session")
        return JsonResponse({"error": "Payment verification error"}, status=400)

    # Verify that payment is completed
    if session.payment_status != "paid":
        return JsonResponse({"error": "Payment not completed"}, status=400)

    # Find the order by session_id
    order = get_object_or_404(Order, stripe_session_id=session_id)

    # If the order is not yet marked as paid, update its status
    if not order.is_paid:
        order.is_paid = True
        order.save()

    # Redirect the user to the frontend URL specified in settings
    return redirect(settings.FRONTEND_URL)

def cancel_view(request):
    return JsonResponse({"message": "Payment cancelled"}, status=200)
