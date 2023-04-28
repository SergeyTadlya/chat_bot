from django.contrib import admin
from .models import Service, MessageHistory, CartInfo, StripePayment, Clients, Chat

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_filter = ['price']


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'created_at']
    list_filter = ['type']


@admin.register(CartInfo)
class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'service', 'quantity']
    list_filter = ['service']


@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_id', 'session_id', 'status']
    list_filter = ['status']


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'need_help', 'is_help', 'is_finished']
    list_filter = ['need_help', 'is_help', 'is_finished']