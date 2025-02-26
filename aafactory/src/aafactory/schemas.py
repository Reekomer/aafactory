from pydantic import BaseModel


class Settings(BaseModel):
    comfy_server_url: str
    comfy_server_port: str
    openai_api_key: str
    elevenlabs_api_key: str
