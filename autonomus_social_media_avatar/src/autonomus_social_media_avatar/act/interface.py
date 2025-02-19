from pathlib import Path
import uuid
from autonomus_social_media_avatar.comfyui.video import send_request_to_generate_video
from autonomus_social_media_avatar.configuration import DB_PATH, DEFAULT_AVATAR_IMAGE_PATH, VOICE_PATH
from autonomus_social_media_avatar.database.manage_db import AVATAR_TABLE_NAME
import gradio as gr
from tinydb import TinyDB
import soundfile as sf


def create_act_interface():
    with gr.Blocks() as act:
        with gr.Accordion("Audio to Video"):
            with gr.Row():
                with gr.Column():
                    avatar_image = gr.Textbox(value=DEFAULT_AVATAR_IMAGE_PATH, visible=False)
                    avatar_animation = gr.Video(value=DEFAULT_AVATAR_IMAGE_PATH, autoplay=True)
                with gr.Column():
                    audio_file = gr.Audio(label="Audio File")
            btn_generate_video = gr.Button("Generate Video")
            btn_generate_video.click(fn=_generate_video, inputs=[audio_file, avatar_image], outputs=[avatar_animation])

        act.load(
            fn=_load_avatar_infos_for_chat,
            outputs=[avatar_animation, avatar_image]
        )
    return act


async def _generate_video(audio_file_bytes: bytes, avatar_image_str: bytes) -> str:
    # Save the audio file
    sample_rate, audio_data = audio_file_bytes  # Unpack the tuple
    audio_file_path = VOICE_PATH / f"{uuid.uuid4().hex}.mp3"
    audio_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save using soundfile
    sf.write(str(audio_file_path), audio_data, sample_rate)
    avatar_image_path = Path(avatar_image_str)
    video_response = await send_request_to_generate_video(avatar_image_path, audio_file_path)
    return video_response


def _load_avatar_infos_for_chat() -> str:
    db = TinyDB(DB_PATH)
    table = db.table(AVATAR_TABLE_NAME)
    avatar_info = table.get(doc_id=1) 
    if avatar_info:
        return (
            avatar_info.get("avatar_image_path", ""),
            avatar_info.get("avatar_image_path", "")
        )
    return DEFAULT_AVATAR_IMAGE_PATH, DEFAULT_AVATAR_IMAGE_PATH