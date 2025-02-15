from autonomus_social_media_avatar.comfyui.video import send_request_to_generate_video
from autonomus_social_media_avatar.configuration import AVATAR_IMAGE_PATH
from autonomus_social_media_avatar.database.manage_db import load_avatar_infos
from autonomus_social_media_avatar.fetcher.fetching import send_request_to_open_ai
from autonomus_social_media_avatar.utils.voice import send_request_to_elevenlabs
import gradio as gr
from PIL import Image
from string import Template

CHAT_HISTORY = []
SYSTEM_PROMPT = Template("""
Your name is $name.
Personality:
$personality

Background Knowledge:
$background_knowledge
""")

def create_chat_interface():
    with gr.Blocks() as chat:
        with gr.Row():
            with gr.Column():
                name = gr.Textbox(label="Name", visible=False)
                personality = gr.Textbox(label="Personality", visible=False)
                background_knowledge = gr.Textbox(label="Background Knowledge", visible=False)
                voice_model = gr.Dropdown(label="Voice Model", choices=["elevenlabs", "openai"], visible=False)
                voice_id = gr.Textbox(label="Voice ID", visible=False)
                avatar_animation = gr.Video(value=AVATAR_IMAGE_PATH, autoplay=True)
            with gr.Column():
                chatbot = gr.Chatbot(placeholder="<strong>Your Personal Avatar</strong><br>Ask Me Anything")
                chatbot.like(vote, None, None)
                msg = gr.Textbox(label="Message")
                submit_btn = gr.Button("Send")
                submit_btn.click(
                    fn=send_request_to_llm,
                    inputs=[msg, name, personality, background_knowledge, voice_model, voice_id],
                    outputs=[msg, chatbot, avatar_animation]
                )
                # Add refresh event
        chat.load(
            fn=load_avatar_infos,
            outputs=[name, personality, background_knowledge, avatar_animation, voice_model, voice_id]
        )
        return chat

async def send_request_to_llm(user_prompt: str, name: str, personality: str, background_knowledge: str, voice_model: str, voice_id: str) -> tuple[str, list, str]:
    user_message = user_prompt
    if len(CHAT_HISTORY) > 0:
        user_message = CHAT_HISTORY[-1][0] + user_prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.substitute(name=name, personality=personality, background_knowledge=background_knowledge)},
        {"role": "user", "content": user_message},
    ]
    text_response = await send_request_to_open_ai(messages)
    if voice_model == "elevenlabs":
        audio_response = await send_request_to_elevenlabs(text_response, voice_id)
    video_response = await send_request_to_generate_video(AVATAR_IMAGE_PATH, audio_response)
    # Return empty message (to clear input), updated history, and animation path
    CHAT_HISTORY.append([user_prompt, text_response])
    return "", CHAT_HISTORY, video_response

def vote(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: " + data.value["value"])
    else:
        print("You downvoted this response: " + data.value["value"])


def update_avatar_image(image: Image.Image):
    global AVATAR_IMAGE
    AVATAR_IMAGE = image
    return image
