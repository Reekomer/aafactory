from aafactory.database.manage_db import load_avatar_infos, update_avatar_infos
import gradio as gr
from aafactory.configuration import VOICE_LANGUAGES, VOICE_MODELS

def create_avatar_setup_interface() -> tuple[gr.Blocks, gr.Textbox, gr.TextArea, gr.TextArea, gr.Image]:
    """
    Create the avatar setup interface.
    """
    with gr.Blocks() as define_avatar:
        with gr.Accordion("Avatar Infos"):
            gr.Markdown("### Name")
            name = gr.Textbox(show_label=False, info="Enter the name of your avatar")
            gr.Markdown("### Personality")
            personality = gr.TextArea(show_label=False, info="Enter the personality of your avatar")
            gr.Markdown("### Background Knowledge")
            background_knowledge = gr.TextArea(show_label=False, info="Enter the background knowledge of your avatar")
            gr.Markdown("### Avatar Image")
            avatar_image = gr.Image(sources=["upload"], type="pil", show_label=False, show_download_button=False, show_fullscreen_button=False)
        with gr.Accordion("Voice Settings"):
            gr.Markdown("### Voice Model")
            voice_model = gr.Dropdown(choices=VOICE_MODELS, value="elevenlabs", interactive=True, info="Select the voice model you want to use")
            voice_id = gr.Textbox(show_label=False, visible=False, interactive=True, info="Enter the voice id you want to use")
            voice_recording = gr.Audio(show_label=False, visible=False, interactive=True, label="Upload a voice sample")
            audio_transcript = gr.TextArea(show_label=False, visible=False, interactive=True, info="Enter the audio transcript you want to use")
            voice_language = gr.Dropdown(choices=VOICE_LANGUAGES, value="en-us", visible=False, interactive=True, info="Select the voice language you want to use")
        
        submit_btn = gr.Button("Save Avatar Infos")
        submit_btn.click(
            fn=update_avatar_infos,
            inputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id, voice_recording, audio_transcript, voice_language]
        )
        voice_model.change(
            fn=adapt_ui_to_voice_model,
            inputs=[voice_model],
            outputs=[voice_id, voice_recording, audio_transcript, voice_language]
        )
        # Add refresh event
        define_avatar.load(
            fn=load_avatar_infos,
            outputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id, voice_recording, audio_transcript, voice_language]
        )
    return define_avatar, name, personality, background_knowledge, avatar_image


def adapt_ui_to_voice_model(voice_model: str) -> tuple[gr.Textbox, gr.Audio, gr.TextArea]:
    """
    Adapt the UI to the voice model.
    """
    if voice_model == "elevenlabs":
        return gr.Textbox(show_label=False, visible=True, interactive=True, info="Enter the voice id you want to use"), gr.Audio(show_label=False, visible=False, interactive=True, label="Upload a voice sample"), gr.TextArea(show_label=False, visible=False, interactive=True, info="Enter the audio transcript you want to use"), gr.Dropdown(choices=VOICE_LANGUAGES, visible=False, interactive=True, info="Select the voice language you want to use")
    if voice_model == "zonos":
        gr.Markdown("### Clone a voice")
        return gr.Textbox(show_label=False, visible=False, interactive=True, info="Enter the voice id you want to use"), gr.Audio(show_label=False, visible=True, interactive=True, label="Upload a voice sample"), gr.TextArea(show_label=False, visible=True, interactive=True, info="Enter the audio transcript you want to use"), gr.Dropdown(choices=VOICE_LANGUAGES, visible=True, interactive=True, info="Select the voice language you want to use")
    if voice_model == "":
        return gr.Textbox(show_label=False, visible=True, interactive=True, info="Enter the voice id you want to use"), gr.Audio(show_label=False, visible=False, interactive=True, label="Upload a voice sample"), gr.TextArea(show_label=False, visible=False, interactive=True, info="Enter the audio transcript you want to use"), gr.Dropdown(choices=VOICE_LANGUAGES, visible=False, interactive=True, info="Select the voice language you want to use")
    raise ValueError(f"Voice model {voice_model} not supported")