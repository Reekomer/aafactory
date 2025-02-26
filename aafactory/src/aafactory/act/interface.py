from pathlib import Path
import uuid
from aafactory.comfyui.video import send_request_to_generate_video
from aafactory.configuration import DB_PATH, DEFAULT_AVATAR_IMAGE_PATH, VOICE_PATH
from aafactory.database.manage_db import AVATAR_TABLE_NAME
import gradio as gr
from tinydb import TinyDB
import soundfile as sf


def create_act_interface():
    with gr.Blocks() as act:
        gr.Markdown("Coming Soon ...")