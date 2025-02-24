import json
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            line_items = []

            for item in data['products']:
                # Convert price to cents (Stripe accepts price as an integer)
                unit_amount = int(item['price'])
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item['name']},
                        'unit_amount': unit_amount,
                    },
                    'quantity': item['quantity'],
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url="http://localhost:3000/success",
                cancel_url="http://localhost:3000/cancel",
            )

            return JsonResponse({'url': session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
