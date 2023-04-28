# stripe payment
from django.views.decorators.csrf import csrf_exempt
from chat_bot_app.models import CartInfo, MessageHistory, StripePayment, Clients
from chat_bot_app.helpers.messages import LastMessage
from django.shortcuts import redirect
from django.http import JsonResponse
import stripe
import json
from chat_bot_project.settings import env


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def stripe_pay(request):
    if request.method == "POST" and is_ajax(request=request):
        # append services for stripe api
        user_email = request.POST.get('user_email')
        services_array = json.loads(request.POST.getlist('services')[0])
        line_items = []
        for service in services_array:
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': service['price'],
                    'product_data': {
                        'name': service['name']
                    }
                },
                'quantity': service['quantity'],
            })

        # Create new Checkout Session for the order
        site_url = env('BOT_URL')
        stripe.api_key = env('STRIPE_SECRET_KEY')
        success_url = site_url + '/stripe/success/?session_id={CHECKOUT_SESSION_ID}'
        cancelled_url = site_url + '/stripe/cancel/?session_id={CHECKOUT_SESSION_ID}'
        checkout_session = stripe.checkout.Session.create(
            success_url=f'{success_url}&email={user_email}',
            cancel_url=f'{cancelled_url}&email={user_email}',
            payment_method_types=['card'],
            mode='payment',
            locale='en',
            line_items=line_items
        )

        # save payment info in database
        defaults = {
            'services': line_items,
        }
        StripePayment.objects.update_or_create(
            user=Clients.objects.get(email=user_email),
            session_id=checkout_session['id'],
            defaults=defaults,
        )
        res = {
            'session_id': checkout_session['id'],
            'public_key': env('STRIPE_PUBLISHABLE_KEY'),
        }
        return JsonResponse(res)


def stripe_pay_success(request):
    # get stripe session id
    stripe.api_key = env('STRIPE_SECRET_KEY')
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)

    success_text = f'Pay "{session["payment_intent"]}" is success. Thanks for buy our services'
    email = request.GET.get('email')
    user = Clients.objects.get(email=email)

    # update stripe payment (added payment_id)
    StripePayment.objects.filter(user=user, session_id=checkout_session_id).update(payment_id=session["payment_intent"], status="success")
    # create message in chat
    MessageHistory.objects.create(user=user, message=success_text, type="bot")
    # delete services in cart
    cart_info = CartInfo.objects.filter(user=user)
    for service in cart_info:
        service.delete()

    LastMessage.save(user)
    return redirect(f"{env('SITE_URL')}/?pay_status=success&email={email}")


def stripe_pay_cancelled(request):
    # get stripe session id
    checkout_session_id = request.GET.get('session_id', None)

    cancelled_text = "Pay is cancelled"
    email = request.GET.get('email')
    user = Clients.objects.get(email=email)
    # create message in chat
    MessageHistory.objects.create(user=user, message=cancelled_text, type="bot")
    StripePayment.objects.filter(user=user, session_id=checkout_session_id).update(status="cancel")

    LastMessage.save(user)
    return redirect(f"{env('SITE_URL')}/?pay_status=cancel&email={email}")