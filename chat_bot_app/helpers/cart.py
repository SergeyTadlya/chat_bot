from chat_bot_app.models import Service


# add services in cart
class AddtoCart:
    @staticmethod
    def services(id, quantity):
        service = Service.objects.get(id=id)
        service_block = \
                f'<div class="chat-cart__purchase" id={id}>' \
                    f'<div class="purchase__info">' \
                        f'<div class="purchase__description">' \
                            f'<p>{service.name}</p>' \
                        f'</div>' \
                        f'<button class="purchase__remove">' \
                            f'<img class="purchase__remove-icon" src="/static/img/close-red.svg" alt="remove">' \
                        f'</button>' \
                    f'</div>' \
                    f'<div class="purchase__price" data-price="{service.price}">' \
                        f'<div class="purchase__count">' \
                            f'<button class="purchase__button count--remove">-</button>' \
                                f'<input class="purchase__price-field" type="text" value="{quantity}">' \
                            f'<button class="purchase__button count--add">+</button>' \
                        f'</div>' \
                        f'<p class="purchase__price-value">{service.price} €</p>' \
                    f'</div>' \
                f'</div>'
        return service_block