# send messages from bot and user in chat widget
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from chat_bot_app.helpers.dialogflow import DialogflowBot
from chat_bot_app.helpers.messages import Messages, LastMessage
from chat_bot_app.models import MessageHistory, Clients, Chat


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def send_user_message(request):
    if request.method == "POST" and is_ajax(request=request):
        text_to_be_analyzed = request.POST.get('user_message')

        user_email = request.POST.get('user_email')
        user = Clients.objects.get(email=user_email)
        # user messages
        user_message_block = Messages.user(text_to_be_analyzed)
        MessageHistory.objects.create(user=user, message=text_to_be_analyzed, type="user")

        current_chat = Chat.objects.get(user=user)
        username = user.email
        # manager answer (blocked bot)
        if current_chat.need_help == True:
            message_text = ""
            message_block = ""
            type = "manager"
        else:
            type = "bot"
            # bot answer from dialogflow (services list)
            response = DialogflowBot.send_message(text_to_be_analyzed)
            # services list (custom answer)
            if response.query_result.intent.display_name == "Services":
                services_answer = Messages.services()
                message_text = services_answer['text']
                message_block = services_answer['block']
                if message_text == "services":
                    message = "services"
                else:
                    message = message_text

                MessageHistory.objects.create(user=user, message=message, type="bot")
            # services list (answer from dialogflow but update info in chat model)
            elif response.query_result.intent.display_name == "Support":
                message_text = response.query_result.fulfillment_text
                message_block = Messages.other(message_text)
                MessageHistory.objects.create(user=user, message=message_text, type="bot")
                Chat.objects.filter(user=user).update(need_help=True)
            # another (answer from dialogflow)
            else:
                message_text = response.query_result.fulfillment_text
                message_block = Messages.other(message_text)
                MessageHistory.objects.create(user=user, message=message_text, type="bot")
            # detected_intent = response.query_result.intent.display_name
            # detected_intent_confidence = response.query_result.intent_detection_confidence

        LastMessage.save(user)
        res = {
            'user_message_text': text_to_be_analyzed,
            'user_message_block': user_message_block,
            'message_text': message_text,
            'message_block': message_block,
            'username': username,
            'type': type,
            'chat_id': current_chat.id,
        }
        return JsonResponse(res)