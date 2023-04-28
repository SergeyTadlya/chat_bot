# main page
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def chat_bot(request):
    return render(request, "chat_bot.html")