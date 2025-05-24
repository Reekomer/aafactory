from openai import BaseModel
from openai import OpenAI
import re
from database.manage_db import get_settings

async def send_request_to_open_ai(messages: list[dict[str, str]]) -> BaseModel:
    """
    Send a request to the OpenAI API.
    """
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o", # gpt-4o-mini
        messages=messages,
        temperature=1.0,
        top_p=1.0,
    )
    raw_content = response.choices[0].message.content
    content_without_double_asterisks = re.sub(r'\*\*', '', raw_content)
    return content_without_double_asterisks
