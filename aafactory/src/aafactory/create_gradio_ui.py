from configuration import DB_PATH, AVATAR_VOICE_RECORDINGS_PATH
from act.interface import create_act_interface
from avatar.interface import create_avatar_setup_interface
from chat.interface import create_chat_interface
from react.interface import create_react_interface
from settings import create_settings
from style import CSS
from utils.interface import create_utils_interface
import gradio as gr
import asyncio

async def create_gradio_interface():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.touch()
    AVATAR_VOICE_RECORDINGS_PATH.mkdir(parents=True, exist_ok=True)
    with gr.Blocks() as simulation:
        with gr.Tabs():
            with gr.Tab(label="Avatar"):  
                create_avatar_setup_interface()
            with gr.Tab(label="Chat"):  
                create_chat_interface()
            with gr.Tab(label="React"):
                create_react_interface()
            with gr.Tab(label="Act"):
                create_act_interface()
            with gr.Tab(label="Utils"):
                create_utils_interface()
            with gr.Tab(label="Settings"):
                create_settings()
    return simulation


if __name__ == "__main__":
    app = asyncio.run(create_gradio_interface())
    app.launch(share=False)
    