# add services in cart or update quantity
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from chat_bot_app.helpers.cart import AddtoCart
from chat_bot_app.models import Service, CartInfo, Clients


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def add_service_to_cart(request):
    if request.method == "POST" and is_ajax(request=request):
        service_id = request.POST.get('service_id')
        user_email = request.POST.get('user_email')
        service_info = Service.objects.get(id=service_id)
        user_info = Clients.objects.get(email=user_email)

        cart_item, created = CartInfo.objects.get_or_create(user=user_info, service=service_info)
        if(created == False):
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()

        res = {
            'added_service_block': AddtoCart.services(service_id, int(cart_item.quantity)),
            'added_service_id': service_id
        }
        return JsonResponse(res)


@csrf_exempt
def update_cart(request):
    if request.method == "POST" and is_ajax(request=request):
        service_count = request.POST.get('service_count')
        functions = request.POST.get('functions')
        user_email = request.POST.get('user_email')
        service_id = request.POST.get('service_id')

        user_info = Clients.objects.get(email=user_email)
        service_info = Service.objects.get(id=service_id)

        try:
            cart_info = CartInfo.objects.get(user=user_info, service=service_info)
            exist = f"cart info {cart_info.id} is exist"
            # delete service in cart from X
            if(service_count == "remove"):
                cart_info.delete()
            # delete service in cart from -
            elif (service_count == "1" and functions == "-"):
                cart_info.delete()
            # update service in cart from +
            else:
                cart_info.quantity = service_count
                cart_info.save()
        except CartInfo.DoesNotExist:
            exist = f"cart info {service_id} does not exist"

        res = {
            'service_id': service_id,
            'service_count': service_count,
            'user_email': user_email,
            'exist': exist,
        }
        return JsonResponse(res)