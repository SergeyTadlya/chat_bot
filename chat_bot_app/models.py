from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to='services')
    price = models.CharField(max_length=50, null=True, blank=True)
    detail_page = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Create date', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Clients(models.Model):
    email = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class MessageHistory(models.Model):
    user = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.DO_NOTHING)
    message = models.TextField(null=True, blank=True)
    type = models.CharField(null=True, blank=True, max_length=100)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Create date', auto_now_add=True)

    def __str__(self):
        return f'{self.pk} Message from {self.user}'

    class Meta:
        verbose_name = 'ChatBot Message'
        verbose_name_plural = 'ChatBot Messages'


class CartInfo(models.Model):
    user = models.ForeignKey(Clients, verbose_name='User', on_delete=models.DO_NOTHING)
    service = models.ForeignKey(Service, verbose_name='Service', on_delete=models.DO_NOTHING)
    quantity = models.FloatField(verbose_name='Quantity', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Create date', auto_now_add=True)

    def __str__(self):
        return f'Cart History: {self.user}'

    class Meta:
        verbose_name = 'Cart Info'


class StripePayment(models.Model):
    user = models.ForeignKey(Clients, verbose_name='User', on_delete=models.DO_NOTHING)
    session_id = models.CharField(null=True, blank=True, max_length=500)
    payment_id = models.CharField(null=True, blank=True, max_length=500)
    services = models.JSONField(verbose_name='Purchased services', blank=True, null=True, default=list)
    status = models.CharField(null=True, blank=True, max_length=100)
    created_at = models.DateTimeField(verbose_name='Create date', auto_now_add=True)

    def __str__(self):
        return f'Stripe Payment: {self.user}'

    class Meta:
        verbose_name = 'Stripe Payment'


class Chat(models.Model):
    user = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.DO_NOTHING)
    last_message = models.ForeignKey(MessageHistory, on_delete=models.DO_NOTHING, null=True, blank=True)
    need_help = models.BooleanField(verbose_name="Need manager help (yes/no)", default=False, null=True)
    is_help = models.BooleanField(verbose_name="Manager is already helping (yes/no)", default=False, null=True)
    is_finished = models.BooleanField(verbose_name="End of manager help (yes/no)", default=True, null=True)
    created_at = models.DateTimeField(verbose_name='Create date', auto_now_add=True)

    def __str__(self):
        return f'Chat: {self.user}'

    class Meta:
        verbose_name = 'Chat'