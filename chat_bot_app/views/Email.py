# email verification
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
from django.http import JsonResponse
from chat_bot_app.helpers.messages import Messages, LastMessage
from chat_bot_app.helpers.cart import AddtoCart
from chat_bot_app.models import CartInfo, MessageHistory, Clients, Chat
from validate_email import validate_email


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def send_email(request):
    if request.method == "POST" and is_ajax(request=request):
        email = request.POST.get('email')
        is_valid = validate_email(email)
        message_history = ""
        total_quantity = ""
        services_in_cart = ""
        first_message_block = ""
        get_chat_id = ""

        # if enter email is valid
        if is_valid == True:
            total_quantity = 0
            services_in_cart = ""

            # get or create user
            # password = email.rsplit('@')[0] + "pass"
            # user, created = User.objects.get_or_create(
            #     email=email,
            #     defaults={'username': email, 'password': make_password(password)},
            # )
            user, created = Clients.objects.get_or_create(email=email)

            if(created == False):
                # recovery of saved messages
                history = MessageHistory.objects.filter(user=user).order_by('created_at')
                if history.exists():
                    message_history = []
                    for message_item in history:
                        if(message_item.type == "bot"):
                            if(message_item.message == "services"):
                                message_history.append(Messages.services()['block'])
                            else:
                                message_history.append(Messages.other(message_item.message))
                        elif(message_item.type == "user"):
                            message_history.append(Messages.user(message_item.message))
                        else:
                            message_history.append(Messages.other(message_item.message))

                # recovery of saved services in cart
                get_cart = CartInfo.objects.filter(user=user)
                if get_cart.exists():
                    quantity = 0
                    services_in_cart = []
                    for service_in_cart in get_cart:
                        quantity += service_in_cart.quantity
                        total_quantity = int(quantity)
                        services_in_cart.append(AddtoCart.services(service_in_cart.service.id, int(service_in_cart.quantity)))

            # first message from bot
            welcome_message = "Welcome to our chat bot"
            get_history, history_created = MessageHistory.objects.get_or_create(
                user=user,
                message=welcome_message,
                type="bot"
            )
            if (history_created == True):
                first_message_block = Messages.other(welcome_message)

            LastMessage.save(user)
            # get chat id for websocket connection
            get_chat_id = Chat.objects.get(user=user).id
        # email is not valid
        else:
            first_message_block = Messages.other("Invalid Email")

        res = {
            'email_block': f'Your email is <span id="saved-email">{email}</span>',
            'first_message_block': first_message_block,
            'message_history': message_history,
            'quantity_service_in_cart': total_quantity,
            'services_in_cart': services_in_cart,
            'is_valid': is_valid,
            'chat_id': get_chat_id,
        }
        return JsonResponse(res)