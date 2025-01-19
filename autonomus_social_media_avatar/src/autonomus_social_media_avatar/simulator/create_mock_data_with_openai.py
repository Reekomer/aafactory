#%%
import os
import json
from autonomus_social_media_avatar.fetcher.environment_objects import AvatarEnvironment
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()   

client = OpenAI(api_key=os.getenv("EXPERIMENT_OPENAI_API_KEY"))

PROMPT = """
I want to create mock data for my project of Aristotle's avatar. At first, the value of the needs should be low. Aristotle just arrived in the world. He is slowly discoring his environment..
He is connected to the internet.
The posts are writtent by other users. Not by Aristotle.
Create a mock data for the avatar environment. It needs to be realistic data. Generate longuer text when it is post content or news content.
The data should be in the format of AvatarEnvironment.

All the values should be between 0 and 1.
"""
response = client.beta.chat.completions.parse(
    model="gpt-4o", # gpt-4o-mini
    messages=[{"role": "user", "content": PROMPT}],
    response_format=AvatarEnvironment
)

response.choices[0].message.parsed
parsed_data = response.choices[0].message.parsed
parsed_data.model_dump_json()


with open("mock_data_new.json", "w") as f:
    json.dump(parsed_data.model_dump(), f)
# %%
