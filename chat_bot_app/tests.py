from django.test import TestCase

# Create your tests here.

# @csrf_exempt
# def webhook(request):
#     if request.method == "GET":
#         return "Not connected to dialogflow"
#     elif request.method == "POST":
#         print("request", request.get())
#         # payload = request.json
#         # user_response = (payload['queryResult']['queryText'])
#         # bot_response = (payload['queryResult']['fulfillmentText'])
#         # if user_response or bot_response != "":
#         #     print("User: " + user_response)
#         #     print("Bot: " + bot_response)
#         return "Message received"
#     else:
#         print(request.data)
#         return "200"


# @csrf_exempt
# def webhook(request):
#     if request.method == "POST":
#         body_unicode = request.body.decode('utf-8')
#         body = json.loads(body_unicode)
#         user_response = body['queryResult']['queryText']
#         bot_response = body['queryResult']['fulfillmentText']
#         print("User: " + user_response)
#         print("Bot: " + bot_response)
#
#         # services = Service.objects.all()
#         # services_items = []
#         # for i, service in enumerate(services):
#         #     services_items.append(
#         #         f'{i+1}) {service.name} - {service.price} €\n'
#         #         f'Detail: {service.detail_page}\n'
#         #         f'Buy: https://buy.com\n\n'
#         #     )
#         # res = {
#         #     'fulfillmentText': "Services list: \n\n" + ''.join(services_items)
#         # }
#         # return JsonResponse(body)
#         res = {
#             'user_message': user_response,
#             'bot_message': bot_response,
#             'dialogflow': "true",
#         }
#         return render(request, "chat_bot.html", res)


#     if request.method == "POST":
        # print('request', request)
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\Programming\Frameworks\chat_bot\media\dialogflow\mokesciusrautasbot-bhn9-56d99b41bc89.json"
        #
        # DIALOGFLOW_PROJECT_ID = 'mokesciusrautasbot-bhn9'
        # DIALOGFLOW_LANGUAGE_CODE = 'en'
        # SESSION_ID = 'me'
        #
        # text_to_be_analyzed = "hello"
        #
        # session_client = dialogflow.SessionsClient()
        # session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        # text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        # query_input = dialogflow.types.QueryInput(text=text_input)
        # try:
        #     response = session_client.detect_intent(session=session, query_input=query_input)
        # except InvalidArgument:
        #     raise
        #
        # print("Query text:", response.query_result.query_text)
        # print("Detected intent:", response.query_result.intent.display_name)
        # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        # print("Fulfillment text:", response.query_result.fulfillment_text)

    # return render(request, "chat_bot.html")

    # views під циклом сервісів (старий шаблон виведення сервісів)
#     services_items.append(\
#         f'<ul class="messages__list">' \
#             f'<li class="messages__item">' \
#                 f'<p class="message-service">{service.name} - {service.price} €</p>' \
#                 f'<span><a href="{service.detail_page}" class="message message--check" target="_blank">Detail</a></span>&nbsp;' \
#                 f'<span><a href="#" class="message message--check">Add to busket</a></span>' \
#             f'</li>' \
#         f'</ul>'
#     )
#
# bot_message_text = "services"
# bot_message_block = ''.join(services_items)
