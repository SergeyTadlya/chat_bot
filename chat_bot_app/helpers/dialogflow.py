import dialogflow_v2 as dialogflow
import os
from chat_bot_project.settings import env


# dialogflow integration with django
class DialogflowBot:
    @staticmethod
    def send_message(message):
        """message sent by the user in the chat"""
        # json_file_url = "D:\Programming\Frameworks\chat_bot\static\dialogflow\mokesciusrautasbot.json"
        json_file_url = env('DIALOGFLOW_JSON_FILE')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_file_url

        DIALOGFLOW_PROJECT_ID = env('DIALOGFLOW_PROJECT_ID')
        # DIALOGFLOW_PROJECT_ID = "mokesciusrautasbot-bhn9"
        DIALOGFLOW_LANGUAGE_CODE = 'en'
        SESSION_ID = 'me'
        text_to_be_analyzed = message

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        return response