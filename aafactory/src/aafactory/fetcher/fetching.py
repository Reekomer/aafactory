from openai import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("EXPERIMENT_OPENAI_API_KEY"))

async def send_request_to_open_ai(messages: list[dict[str, str]]) -> BaseModel:
    response = client.chat.completions.create(
        model="gpt-4o", # gpt-4o-mini
        messages=messages,
        temperature=1.0,
        top_p=1.0,
    )
    return response.choices[0].message.content
