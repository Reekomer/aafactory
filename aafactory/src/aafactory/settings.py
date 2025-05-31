from configuration import DB_PATH
from schemas import Settings
from dotenv import load_dotenv
import gradio as gr
import os
from loguru import logger
from tinydb import TinyDB

load_dotenv()

def create_settings():
    with gr.Blocks() as settings:
        gr.Markdown("## Settings")
        with gr.Accordion("Comfy UI", open=False):
            comfy_server_url = gr.Textbox(label="ComfyUI Server URL", value=os.getenv("COMFYUI_SERVER_URL"), interactive=True)
            comfy_server_port = gr.Textbox(label="ComfyUI Server Port", value=os.getenv("COMFYUI_SERVER_PORT"), interactive=True)
        with gr.Accordion("ElevenLabs", open=False):
            elevenlabs_api_key = gr.Textbox(label="ElevenLabs API Key", value=os.getenv("ELEVENLABS_API_KEY"), interactive=True)
        with gr.Accordion("LLM", open=False):
            openai_api_key = gr.Textbox(label="OpenAI API Key", value=os.getenv("OPENAI_API_KEY"), interactive=True)

        submit_btn = gr.Button("Save Settings")
        submit_btn.click(
            fn=_save_settings_to_db, 
            inputs=[comfy_server_url, comfy_server_port, openai_api_key, elevenlabs_api_key],
            outputs=[comfy_server_url, comfy_server_port, openai_api_key, elevenlabs_api_key]
        )
    settings.load(
        fn=_load_settings_from_db,
        outputs=[comfy_server_url, comfy_server_port, openai_api_key, elevenlabs_api_key]
    )

def _save_settings_to_db(*args):
    settings = Settings(
        comfy_server_url=args[0],
        comfy_server_port=args[1],
        openai_api_key=args[2],
        elevenlabs_api_key=args[3]
    )
    db = TinyDB(DB_PATH)
    db.table("settings").truncate()
    db.table("settings").insert(settings.model_dump())
    logger.success("Settings saved")
    settings_dict = settings.model_dump()
    return [settings_dict[key] for key in [
        'comfy_server_url', 'comfy_server_port', 'openai_api_key',
        'elevenlabs_api_key'
    ]]

def _load_settings_from_db():
    db = TinyDB(DB_PATH)
    settings_dict = db.table("settings").get(doc_id=1)
    if settings_dict is None:
        return [None, None, None, None]
    return [settings_dict[key] for key in [
        'comfy_server_url', 'comfy_server_port', 'openai_api_key',
        'elevenlabs_api_key'
    ]]