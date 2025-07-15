from pathlib import Path
from comfyui.video import send_request_to_generate_video
from configuration import AVATAR_PAGE_SETTINGS_TABLE_NAME, DB_PATH, DEFAULT_AVATAR_IMAGE_PATH, VOICE_MODELS
from database.manage_db import AVATAR_TABLE_NAME
from fetcher.fetching import send_request_to_open_ai
from utils.voice import send_request_to_elevenlabs, send_request_to_zonos
import gradio as gr
from PIL import Image
from string import Template

from tinydb import TinyDB

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
                voice_model = gr.Dropdown(label="Voice Model", choices=VOICE_MODELS, visible=False)
                voice_id = gr.Textbox(label="Voice ID", visible=False)
                voice_language = gr.Textbox(label="Voice Language", visible=False)
                voice_recording_path = gr.Textbox(label="Voice Recording", visible=False)
                audio_transcript = gr.Textbox(label="Audio Transcript", visible=False)
                avatar_image = gr.Textbox(value=DEFAULT_AVATAR_IMAGE_PATH, visible=False)
                avatar_animation = gr.Video(value=DEFAULT_AVATAR_IMAGE_PATH, autoplay=True)
            with gr.Column():
                chatbot = gr.Chatbot(placeholder="<strong>Your Personal Avatar</strong><br>Ask Me Anything")
                chatbot.like(vote, None, None)
                msg = gr.Textbox(label="Message")
                submit_btn = gr.Button("Send")
                submit_btn.click(
                    fn=send_request_to_llm,
                    inputs=[avatar_image, msg, name, personality, background_knowledge, voice_model, voice_id, voice_recording_path, audio_transcript, voice_language],
                    outputs=[msg, chatbot, avatar_animation]
                )
                # Add refresh event
        chat.load(
            fn=_load_avatar_infos_for_chat,
            outputs=[name, personality, background_knowledge, avatar_animation, voice_model, voice_id, voice_recording_path, audio_transcript, voice_language, avatar_image]
        )
        return chat


def _load_avatar_infos_for_chat():
    db = TinyDB(DB_PATH)
    table = db.table(AVATAR_TABLE_NAME)
    avatar_page_settings_table = db.table(AVATAR_PAGE_SETTINGS_TABLE_NAME)
    avatar_page_settings = avatar_page_settings_table.get(doc_id=1)  # Changed from 0 to 1 since TinyDB starts at 1
    avatar_name = avatar_page_settings.get("avatar_name")
    avatar_info = table.get(lambda x: x.get("name") == avatar_name) 
    if avatar_info:
        return (
            avatar_info.get("name", ""),
            avatar_info.get("personality", ""),
            avatar_info.get("background_knowledge", ""),
            avatar_info.get("avatar_image_path", "") ,  # for video
            avatar_info.get("voice_model", "elevenlabs"),
            avatar_info.get("voice_id", ""),
            avatar_info.get("voice_recording_path", ""),
            avatar_info.get("audio_transcript", ""),
            avatar_info.get("voice_language", ""),
            avatar_info.get("avatar_image_path", "")  # for image path
        )
    return "", "", "", DEFAULT_AVATAR_IMAGE_PATH, "elevenlabs", "", "", "", "", ""

async def send_request_to_llm(avatar_image_path: str, user_prompt: str, name: str, personality: str, background_knowledge: str, voice_model: str, voice_id: str, voice_recording_path: str, audio_transcript: str, voice_language: str) -> tuple[str, list, str]:
    user_message = user_prompt
    avatar_image_path = Path(avatar_image_path)
    if len(CHAT_HISTORY) > 0:
        user_message = CHAT_HISTORY[-1][0] + user_prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.substitute(name=name, personality=personality, background_knowledge=background_knowledge)},
        {"role": "user", "content": user_message},
    ]
    text_response = await send_request_to_open_ai(messages)
    if voice_model == "elevenlabs":
        audio_response = await send_request_to_elevenlabs(text_response, voice_id)
    elif voice_model == "zonos":
        audio_response = await send_request_to_zonos(text_response, voice_language, voice_recording_path, audio_transcript)
    video_response = await send_request_to_generate_video(avatar_image_path, audio_response)
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
