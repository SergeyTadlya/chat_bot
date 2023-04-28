from chat_bot_app.models import Service, MessageHistory, Chat


# send answer from dialogflow in chatbot
class Messages:
    @staticmethod
    def user(message):
        """send message from user"""
        user_message_block = \
            f'<ul class="messages__list messages__list--user">' \
                f'<li class="messages__item">' \
                    f'<p class="message message--user">{message}</p>' \
                f'</li>' \
            f'</ul>'
        return user_message_block

    @staticmethod
    def other(message):
        """send answer from dialogflow about other messages"""
        other_message_block = \
            f'<ul class="messages__list">' \
                f'<li class="messages__item">' \
                    f'<p class="message">{message}</p>' \
                f'</li>' \
            f'</ul>'
        return other_message_block

    @staticmethod
    def services():
        """send custom answer from bot about services"""
        services = Service.objects.all()
        if services.exists():
            services_items = []
            for service in services:
                services_items.append(
                    f'<li>'
                        f'<div class="product">'
                            f'<div class="product__content">'
                                f'<h5 class="product__title">{service.name}</h5>'
                                f'<p class="product__description">{service.price} €</p>'
                                f'<div class="product__buttons-wrapper">'
                                    f'<div class="product__button-block">'
                                        f'<button class="product__button">'
                                            f'<a href="{service.detail_page}" target="_blank">Detail</a>'
                                        f'</button>'
                                    f'</div>'
                                    f'<div class="product__button-block">'
                                        # f'<button class="product__button">'
                                        #     f'<span class="product__button-text" onclick=AddToCart({service.id})>add to cart</span>'
                                        # f'</button>'
                                        f'<button class="product__button" onclick=AddToCart({service.id})>add to cart</button>'
                                    f'</div>'
                                f'</div>'
                            f'</div>'
                        f'</div>'
                    f'</li>'
                )
            services_message_text = "services"
            services_block = ''.join(services_items)
            services_message_block = f'<ul class="product-list">{services_block}</ul>'
        else:
            services_message_text = "We don't have any services available"
            services_message_block = \
                f'<ul class="messages__list">' \
                    f'<li class="messages__item">' \
                        f'<p class="message">{services_message_text}</p>' \
                    f'</li>' \
                f'</ul>'
        return {
            'text': services_message_text,
            'block': services_message_block,
        }


class LastMessage:
    @staticmethod
    def save(client_email):
        """save last message in table from chat"""
        get_chat = Chat.objects.filter(user=client_email)
        get_last_message = MessageHistory.objects.filter(user=client_email).order_by('-created_at').first()
        if get_chat.exists():
            chat = get_chat.update(
                user=client_email,
                last_message=get_last_message,
            )
        else:
            chat = Chat.objects.create(
                user=client_email,
                last_message=get_last_message,
            )
        return chat