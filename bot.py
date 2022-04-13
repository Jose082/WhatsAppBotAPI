import openai
from configuration import OPENAI_API_TOKEN
from constants import BOT_PROMPT, BOT_CONTINUATION, UNIQUE_ID
import pandas as pd
from pathlib import Path
from pydantic.main import BaseModel

from constants import CONVERSATIONS_CSV, REQUIRED, USER_NAME, MESSAGE, CHOICES, TEXT


class Conversation(BaseModel):
    unique_id: str
    user_name: str
    message: str
    # is_finished: bool


class Conversations:
    def __init__(self):
        conversations_file = Path(CONVERSATIONS_CSV)
        if not conversations_file.is_file():
            self.create_conversations()
        self.conversations = self.load_conversations()

    @classmethod
    def create_conversations(cls):
        conversation_schema = Conversation.schema()  # WARN: When optional params required this method doesn't work
        columns = conversation_schema[REQUIRED]
        conversations = pd.DataFrame(columns=columns)
        conversations.to_csv(CONVERSATIONS_CSV, index=False)

    @classmethod
    def load_conversations(cls):
        conversations = pd.read_csv(CONVERSATIONS_CSV)
        return conversations

    def get_conversation(self, unique_id):
        return self.conversations[self.conversations[UNIQUE_ID] == unique_id]

    def put_conversation(self, unique_id, user_name, message):
        conversation = {
            UNIQUE_ID: unique_id,
            USER_NAME: user_name,
            MESSAGE: message
        }
        self.conversations = pd.concat([self.conversations, pd.DataFrame.from_records([conversation])],
                                       ignore_index=True)
        self.conversations.to_csv(CONVERSATIONS_CSV, index=False)
        return conversation


class GPTBot:
    def __init__(self):
        self.conversations = Conversations()
        openai.api_key = OPENAI_API_TOKEN

    def reply(self, unique_id, user_name, message):
        conversation = self.conversations.get_conversation(unique_id=unique_id)
        is_new_conversation = conversation.empty

        prompt = BOT_PROMPT % message if is_new_conversation \
            else conversation[MESSAGE].iloc[0] + BOT_CONTINUATION % message

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Usuario:", " Asistente:"]
        )
        bot_response = response[CHOICES][0][TEXT]
        message = prompt + bot_response

        self.conversations.put_conversation(unique_id=unique_id, user_name=user_name, message=message)

        return bot_response
