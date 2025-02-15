from autonomus_social_media_avatar.configuration import DB_PATH
from autonomus_social_media_avatar.schemas import Settings
from dotenv import load_dotenv
import gradio as gr
import os
from loguru import logger
from tinydb import TinyDB

load_dotenv()

def create_settings():
    gr.Markdown("## Settings")
    with gr.Accordion("APIs & DB", open=False):
        with gr.Accordion("Comfy UI"):
            comfyui_server_ip = gr.Textbox(label="ComfyUI Server IP", value="http://localhost:8188", interactive=True)
            comfyui_server_port = gr.Textbox(label="ComfyUI Server Port", value="8188", interactive=True)
            character_workflow_path = gr.Textbox(label="Character Workflow Path", value="", interactive=True)
            environment_workflow_path = gr.Textbox(label="Environment Workflow Path", value="", interactive=True)

        with gr.Accordion("ElevenLabs"):
            elevenlabs_api_key = gr.Textbox(label="ElevenLabs API Key", value=os.getenv("ELEVENLABS_API_KEY"), interactive=True)
            voice_id = gr.Textbox(label="Voice ID", value=os.getenv("VOICE_ID"), interactive=True)
        with gr.Accordion("Database"):
            create_new_database = gr.Checkbox(label="Create New Database", value=False, interactive=True)

        with gr.Accordion("Other"):
            openai_api_key = gr.Textbox(label="OpenAI API Key", value=os.getenv("EXPERIMENT_OPENAI_API_KEY"), interactive=True)

    submit_btn = gr.Button("Save Settings")
    submit_btn.click(
        fn=_save_settings_to_db, 
        inputs=[comfyui_server_ip, comfyui_server_port, character_workflow_path, 
                environment_workflow_path, create_new_database, openai_api_key, 
                elevenlabs_api_key, voice_id],
        outputs=[comfyui_server_ip, comfyui_server_port, character_workflow_path, 
                environment_workflow_path, create_new_database, openai_api_key, 
                elevenlabs_api_key, voice_id]
    )

def _save_settings_to_db(*args):
    settings = Settings(
        comfyui_server_ip=args[0],
        comfyui_server_port=args[1],
        character_workflow_path=args[2],
        environment_workflow_path=args[3],
        create_new_database=args[4],
        openai_api_key=args[5],
        elevenlabs_api_key=args[6],
        voice_id=args[7]
    )
    db = TinyDB(DB_PATH)
    db.table("settings").truncate()
    db.table("settings").insert(settings.model_dump())
    logger.success("Settings saved")
    settings_dict = settings.model_dump()
    return [settings_dict[key] for key in [
        'comfyui_server_ip', 'comfyui_server_port', 'character_workflow_path',
        'environment_workflow_path', 'create_new_database', 'openai_api_key',
        'elevenlabs_api_key', 'voice_id'
    ]]


***REMOVED***
***REMOVED***