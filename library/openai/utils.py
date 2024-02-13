import tiktoken
from openai import OpenAI
import constants as constants

client = OpenAI(api_key=constants.OPENAI_API_KEY)

# Creates message object for ai
def create_ai_object_message_from_content(content):
    return {
        "role": "ai",
        "content": content
    }

# Creates message object for user
def create_user_object_message_from_content(content):
    return {
        "role": "user",
        "content": content
    }

# Counts the amount of tokens
def tiktoken_count_amount_of_tokens(self, content: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(content))
    return num_tokens

# Openai embeddings
def get_openai_embedding(self, content: str) -> list:
    return client.embeddings.create(input=content, model="text-embedding-ada-002")["data"][0]["embedding"]