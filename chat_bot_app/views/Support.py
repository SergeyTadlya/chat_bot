# communication with the manager
from django.shortcuts import render
from chat_bot_app.models import MessageHistory, Clients, Chat, CartInfo
from chat_bot_app.helpers.messages import Messages, LastMessage
from chat_bot_app.helpers.support import Manager
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def support(request):
    current_chats = []
    chats = Chat.objects.all()
    for chat in chats:
        if chat.need_help == False:
            need_help_style = 'color: black'
        else:
            need_help_style = 'color: red'

        if chat.is_help == True:
            is_help_style = 'color: green'
        else:
            is_help_style = 'color: black'

        services_in_cart = CartInfo.objects.filter(user=chat.user)
        if services_in_cart.exists():
            services = []
            for item in services_in_cart:
                service = {
                    'client': chat.user,
                    'name': item.service,
                    'quantity': item.quantity,
                }
                services.append(service)
        else:
            services = {
                'client': chat.user,
                'name': "",
                'quantity': "",
            }

        current_chats.append({
            'id': chat.id,
            'client': chat.user.email,
            'last_message': chat.last_message.message,
            'need_help': chat.need_help,
            'need_help_style': need_help_style,
            'is_help': chat.is_help,
            'is_help_style': is_help_style,
            'is_finished': chat.is_finished,
            'services': services,
        })
        print(current_chats)
    res = {
        'title': 'Current chat list',
        'current_chats': current_chats,
    }
    return render(request, "support/chat_list.html", res)


def chat_detail(request, id):
    current_chat = Chat.objects.get(id=id)
    user = current_chat.user
    # start & finish button display style
    if current_chat.is_help == True and current_chat.is_finished == False:
        button_start = "none"
        button_finish = "block"
    else:
        button_start = "block"
        button_finish = "none"

    # set saved message histore in page
    message_history = ""
    history = MessageHistory.objects.filter(user=user).order_by('created_at')
    if history.exists():
        message_history = []
        for message_item in history:
            if (message_item.type == "bot"):
                if (message_item.message == "services"):
                    message_history.append(Messages.services()['block'])
                else:
                    message_history.append(Messages.other(message_item.message))
            elif (message_item.type == "user"):
                message_history.append(Messages.user(message_item.message))
            else:
                message_history.append(Messages.other(message_item.message))

    res = {
        'title': f'Chat {user.email}',
        'chat_id': current_chat.id,
        'message_history': message_history,
        'client': user.email,
        'button_start': button_start,
        'button_finish': button_finish,
    }
    return render(request, "support/chat_detail.html", res)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def connecting_manager(request):
    if request.method == "POST" and is_ajax(request=request):
        user_email = request.POST.get('user_email')
        manager_id = request.POST.get('manager_id')
        manager = User.objects.get(id=manager_id)
        if request.POST.get('connecting') == "start":
            manager_connect = Manager.connect_to_chat(user_email, manager_id)
            manager_message_block = manager_connect['manager_message_block']
            manager_message_text = manager_connect['manager_message_text']
            connecting_status = "start"
            type = "manager"
        else:
            manager_disconnect = Manager.disconnect_to_chat(user_email, manager_id)
            manager_message_block = manager_disconnect['manager_message_block']
            manager_message_text = manager_disconnect['manager_message_text']
            connecting_status = "finish"
            type = "bot"

        # save last message about manager connect
        user = Clients.objects.get(email=user_email)
        LastMessage.save(user)
        res = {
            'manager_message_block': manager_message_block,
            'manager_message_text': manager_message_text,
            'connecting_status': connecting_status,
            'username': manager.username,
            'type': type
        }
        return JsonResponse(res)


@csrf_exempt
def send_manager_message(request):
    if request.method == "POST" and is_ajax(request=request):
        message = request.POST.get('manager_message')
        # client info
        client_email = request.POST.get('client_email')
        client = Clients.objects.get(email=client_email)
        # manager info
        manager_id = request.POST.get('manager_id')
        manager = User.objects.get(id=manager_id)

        # send manager messages
        manager_message_block = Messages.other(message)
        MessageHistory.objects.create(
            user=client,
            message=message,
            type="manager",
            manager=manager,
        )
        LastMessage.save(client)
        res = {
            'manager_message_text': message,
            'manager_message_block': manager_message_block,
            'username': manager.username,
        }
        return JsonResponse(res)