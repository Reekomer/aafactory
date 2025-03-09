from aafactory.configuration import DB_PATH
from aafactory.act.interface import create_act_interface
from aafactory.avatar.interface import create_avatar_setup_interface
from aafactory.chat.interface import create_chat_interface
from aafactory.react.interface import create_react_interface
from aafactory.settings import create_settings
from aafactory.style import CSS
from aafactory.utils.interface import create_utils_interface
import gradio as gr
import asyncio


async def create_gradio_interface():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.touch()
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
