from pathlib import Path
import uuid
from aafactory.comfyui.video import send_request_to_generate_video
from aafactory.configuration import DB_PATH, DEFAULT_AVATAR_IMAGE_PATH, VOICE_PATH
from aafactory.database.manage_db import AVATAR_TABLE_NAME
from aafactory.utils.voice import send_request_to_elevenlabs
import gradio as gr
from tinydb import TinyDB
import soundfile as sf


def create_utils_interface():
    with gr.Blocks() as utils:
        with gr.Accordion("Audio to Video", open=False):
            with gr.Row():
                with gr.Column():
                    audio_avatar_image = gr.Textbox(value=DEFAULT_AVATAR_IMAGE_PATH, visible=False)
                    audio_avatar_animation = gr.Video(value=DEFAULT_AVATAR_IMAGE_PATH, autoplay=True)
                with gr.Column():
                    audio_file = gr.Audio(label="Audio File")
            btn_generate_video = gr.Button("Generate Video")
            btn_generate_video.click(fn=_generate_video_from_audio, inputs=[audio_file, audio_avatar_image], outputs=[audio_avatar_animation])
        with gr.Accordion("Script to Video", open=False):
            with gr.Row():
                with gr.Column():
                    script_avatar_image = gr.Textbox(value=DEFAULT_AVATAR_IMAGE_PATH, visible=False)
                    script_avatar_animation = gr.Video(value=DEFAULT_AVATAR_IMAGE_PATH, autoplay=True)
                with gr.Column():
                    gr.Markdown("### Avatar Script")
                    avatar_script = gr.TextArea()
                    gr.Markdown("### Voice Model")
                    voice_model = gr.Dropdown(choices=["elevenlabs", "openai"], value="elevenlabs", interactive=True, info="Select the voice model you want to use")
                    gr.Markdown("### Voice ID")
                    voice_id = gr.Textbox(show_label=False, interactive=True, info="Enter the voice id you want to use")
            btn_generate_video = gr.Button("Generate Video")
            btn_generate_video.click(fn=_generate_video_from_script, inputs=[avatar_script, script_avatar_image, voice_model, voice_id], outputs=[script_avatar_animation])
        

        utils.load(
            fn=_load_avatar_infos_for_chat,
            outputs=[audio_avatar_animation, audio_avatar_image, script_avatar_animation, script_avatar_image]
        )
    return utils


async def _generate_video_from_audio(audio_file_bytes: bytes, avatar_image_str: bytes) -> str:
    # Save the audio file
    sample_rate, audio_data = audio_file_bytes  # Unpack the tuple
    audio_file_path = VOICE_PATH / f"{uuid.uuid4().hex}.mp3"
    audio_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Normalize audio data to float32 between -1 and 1
    audio_data = audio_data.astype('float32')
    if audio_data.max() > 1.0 or audio_data.min() < -1.0:
        audio_data = audio_data / max(abs(audio_data.max()), abs(audio_data.min()))
    
    # Save using soundfile with proper settings
    sf.write(
        str(audio_file_path), 
        audio_data, 
        sample_rate, 
        format='MP3'
    )
    
    avatar_image_path = Path(avatar_image_str)
    video_response = await send_request_to_generate_video(avatar_image_path, audio_file_path)
    return video_response


async def _generate_video_from_script(avatar_script: str, avatar_image_str: str, voice_model: str, voice_id: str) -> str:
    if voice_model == "elevenlabs":
        audio_response = await send_request_to_elevenlabs(avatar_script, voice_id)
    video_response = await send_request_to_generate_video(avatar_image_str, audio_response)
    return video_response


def _load_avatar_infos_for_chat() -> str:
    db = TinyDB(DB_PATH)
    table = db.table(AVATAR_TABLE_NAME)
    avatar_info = table.get(doc_id=1) 
    if avatar_info:
        return (
            avatar_info.get("avatar_image_path", ""),
            avatar_info.get("avatar_image_path", ""),
            avatar_info.get("avatar_image_path", ""),
            avatar_info.get("avatar_image_path", "")
        )
    return DEFAULT_AVATAR_IMAGE_PATH, DEFAULT_AVATAR_IMAGE_PATH, DEFAULT_AVATAR_IMAGE_PATH, DEFAULT_AVATAR_IMAGE_PATH