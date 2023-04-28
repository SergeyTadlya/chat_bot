from django.urls import path
from chat_bot_app.views import *
from django.conf.urls.static import static
from chat_bot_project import settings

urlpatterns = [
    path('', chat_bot, name="chat_bot"),
    # message pages
    path('send_email/', send_email, name='send_email'),
    path('send_user_message/', send_user_message, name='send_user_message'),
    # cart pages
    path('add_service_to_cart/', add_service_to_cart, name='add_service_to_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    # stripe pages
    path('stripe_pay/', stripe_pay, name='stripe_pay'),
    path('stripe/success/', stripe_pay_success, name='stripe_pay_success'),
    path('stripe/cancel/', stripe_pay_cancelled, name='stripe_pay_cancelled'),
    # support pages
    path('support/', support, name='support'),
    path('chat/<int:id>/', chat_detail, name='chat_detail'),
    path('connecting_manager/', connecting_manager, name='connecting_manager'),
    path('send_manager_message/', send_manager_message, name='send_manager_message'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)