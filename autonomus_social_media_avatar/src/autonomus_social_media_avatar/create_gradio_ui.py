from autonomus_social_media_avatar.act.interface import create_act_interface
from autonomus_social_media_avatar.avatar.interface import create_avatar_setup_interface
from autonomus_social_media_avatar.chat.interface import create_chat_interface
from autonomus_social_media_avatar.react.interface import create_react_interface
from autonomus_social_media_avatar.settings import create_settings
from autonomus_social_media_avatar.style import CSS_STYLE
import gradio as gr
import asyncio


async def create_gradio_interface():
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
            with gr.Tab(label="Settings"):
                create_settings()
    return simulation


if __name__ == "__main__":
    app = asyncio.run(create_gradio_interface())
    app.launch(share=False)
