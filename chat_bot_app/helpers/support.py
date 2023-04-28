from chat_bot_app.models import MessageHistory, Clients, Chat
from chat_bot_app.helpers.messages import Messages
from django.contrib.auth.models import User


class Manager:
    @staticmethod
    def connect_to_chat(user_email, manager_id):
        user = Clients.objects.get(email=user_email)
        manager = User.objects.get(id=manager_id)

        # update chat then need manager help
        Chat.objects.filter(user=user).update(is_help=True, is_finished=False)

        # send message about manager connect
        manager_connect_text = "Manager connect to chat"
        MessageHistory.objects.create(
            user=user,
            message=manager_connect_text,
            type="manager",
            manager=manager,
        )
        manager_message_block = Messages.other(manager_connect_text)
        res = {
            'manager_message_block': manager_message_block,
            'manager_message_text': manager_connect_text,
        }
        return res

    @staticmethod
    def disconnect_to_chat(user_email, manager_id):
        user = Clients.objects.get(email=user_email)
        manager = User.objects.get(id=manager_id)

        # update chat then need manager help
        Chat.objects.filter(user=user).update(need_help=False, is_help=False, is_finished=True)

        # send message about manager connect
        manager_connect_text = "Manager disconnect to chat"
        MessageHistory.objects.create(
            user=user,
            message=manager_connect_text,
            type="manager",
            manager=manager,
        )
        manager_message_block = Messages.other(manager_connect_text)
        res = {
            'manager_message_block': manager_message_block,
            'manager_message_text': manager_connect_text,
        }
        return res
