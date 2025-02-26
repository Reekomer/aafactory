from aafactory.database.manage_db import load_avatar_infos, update_avatar_infos
import gradio as gr

def create_avatar_setup_interface() -> tuple[gr.Blocks, gr.Textbox, gr.TextArea, gr.TextArea, gr.Image]:
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
        with gr.Accordion("Voice Settings", open=False):
            gr.Markdown("### Voice Model")
            voice_model = gr.Dropdown(choices=["elevenlabs", "openai"], value="elevenlabs", interactive=True, info="Select the voice model you want to use")
            gr.Markdown("### Voice ID")
            voice_id = gr.Textbox(show_label=False, interactive=True, info="Enter the voice id you want to use")
        
        submit_btn = gr.Button("Save Avatar Infos")
        submit_btn.click(
            fn=update_avatar_infos,
            inputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id]
        )
        # Add refresh event
        define_avatar.load(
            fn=load_avatar_infos,
            outputs=[name, personality, background_knowledge, avatar_image, voice_model, voice_id]
        )
    return define_avatar, name, personality, background_knowledge, avatar_image
