from aafactory.database.manage_db import get_available_avatars, load_avatar_infos, load_selected_avatar_infos, save_avatar_page_settings, update_avatar_infos
import gradio as gr
from aafactory.configuration import VOICE_LANGUAGES, VOICE_MODELS

def create_avatar_setup_interface() -> None:
    """
    Create the avatar setup interface.
    """
    avatar_setup = gr.Row()
    available_avatars = gr.Dropdown(choices=[], visible=False)
    avatar_infos = gr.Accordion(visible=False)
    voice_settings = gr.Accordion(visible=False)
    submit_btn = gr.Button("Save Avatar Infos", visible=False)
    with gr.Blocks() as define_avatar:
        with avatar_setup:
            with gr.Column() as create_avatar:
                create_avatar_btn = gr.Button("Create New Avatar")
                create_avatar_btn.click(
                    fn=_create_avatar_infos,
                    inputs=[],
                    outputs=[avatar_infos, voice_settings, submit_btn]
                )
            with gr.Column() as load_avatar:
                load_avatar_btn = gr.Button("Load Existing Avatar")
                load_avatar_btn.click(
                    fn=_load_available_avatars,
                    inputs=[],
                    outputs=[available_avatars, avatar_infos, voice_settings, submit_btn]
                )
        
        with avatar_infos:
            gr.Markdown("### Name")
            name = gr.Textbox(show_label=False, info="Enter the name of your avatar")
            gr.Markdown("### Personality")
            personality = gr.TextArea(show_label=False, info="Enter the personality of your avatar")
            gr.Markdown("### Background Knowledge")
            background_knowledge = gr.TextArea(show_label=False, info="Enter the background knowledge of your avatar")
            gr.Markdown("### Avatar Image")
            avatar_image = gr.Image(sources=["upload"], type="pil", show_label=False, show_download_button=False, show_fullscreen_button=False)
        with voice_settings:
            gr.Markdown("### Voice Model")
            voice_model = gr.Dropdown(choices=VOICE_MODELS, value="elevenlabs", interactive=True, info="Select the voice model you want to use")
            voice_id = gr.Textbox(show_label=False, visible=False, interactive=True, info="Enter the voice id you want to use")
            voice_recording = gr.Audio(show_label=False, visible=False, interactive=True, label="Upload a voice sample")
            audio_transcript = gr.TextArea(show_label=False, visible=False, interactive=True, info="Enter the audio transcript you want to use")
            voice_language = gr.Dropdown(choices=VOICE_LANGUAGES, value="en-us", visible=False, interactive=True, info="Select the voice language you want to use")
        available_avatars.change(
            fn=load_selected_avatar_infos,
            inputs=[available_avatars],
            outputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id, voice_recording, audio_transcript, voice_language]
        )
        submit_btn.click(
            fn=update_avatar_infos,
            inputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id, voice_recording, audio_transcript, voice_language]
        )
        voice_model.change(
            fn=_adapt_ui_to_voice_model,
            inputs=[voice_model],
            outputs=[voice_id, voice_recording, audio_transcript, voice_language]
        )
        # Add refresh event
        define_avatar.load(
            fn=load_avatar_infos,
            inputs=[],
            outputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id, voice_recording, audio_transcript, voice_language]
        )

def _load_available_avatars() -> tuple[gr.Dropdown, gr.Accordion, gr.Accordion, gr.Button]:
    """
    Load the available avatars.
    """
    save_avatar_page_settings(False)
    available_avatars = get_available_avatars()
    return gr.Dropdown(choices=available_avatars, interactive=True, visible=True), gr.Accordion("Avatar Infos", visible=True), gr.Accordion("Voice Settings", visible=True), gr.Button("Save Avatar Infos", visible=True)   


def _adapt_ui_to_voice_model(voice_model: str) -> tuple[gr.Textbox, gr.Audio, gr.TextArea]:
    """
    Adapt the UI to the voice model.
    """
    if voice_model == "elevenlabs":
        return gr.Textbox(show_label=False, visible=True, interactive=True, info="Enter the voice id you want to use"), gr.Audio(show_label=False, visible=False, interactive=True, label="Upload a voice sample"), gr.TextArea(show_label=False, visible=False, interactive=True, info="Enter the audio transcript you want to use"), gr.Dropdown(choices=VOICE_LANGUAGES, value="en-us", visible=False, interactive=True, info="Select the voice language you want to use")
    if voice_model == "zonos":
        gr.Markdown("### Clone a voice")
        return gr.Textbox(show_label=False, visible=False, interactive=True, info="Enter the voice id you want to use"), gr.Audio(show_label=False, visible=True, interactive=True, label="Upload a voice sample"), gr.TextArea(show_label=False, visible=True, interactive=True, info="Enter the audio transcript you want to use"), gr.Dropdown(choices=VOICE_LANGUAGES, value="en-us", visible=True, interactive=True, info="Select the voice language you want to use")
    if voice_model == "":
        return gr.Textbox(show_label=False, visible=True, interactive=True, info="Enter the voice id you want to use"), gr.Audio(show_label=False, visible=False, interactive=True, label="Upload a voice sample"), gr.TextArea(show_label=False, visible=False, interactive=True, info="Enter the audio transcript you want to use"), gr.Dropdown(choices=VOICE_LANGUAGES, value="en-us", visible=False, interactive=True, info="Select the voice language you want to use")
    raise ValueError(f"Voice model {voice_model} not supported")

def _create_avatar_infos() -> tuple[gr.Accordion, gr.Accordion, gr.Button]:
    """
    Create the avatar infos.
    """
    save_avatar_page_settings(True)
    gr.Info("Creating new avatar. Please reload the page to empty the fields.",)
    return gr.Accordion("Avatar Infos", visible=True), gr.Accordion("Voice Settings", visible=True), gr.Button("Save Avatar Infos", visible=True)

