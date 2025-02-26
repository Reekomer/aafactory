from pydantic import BaseModel


class Settings(BaseModel):
    comfyui_server_ip: str
    comfyui_server_port: str
    character_workflow_path: str
    environment_workflow_path: str
    create_new_database: bool
    openai_api_key: str
    elevenlabs_api_key: str
    voice_id: str