import gradio as gr
from pathlib import Path

SITUATION_SUMMARY = "Aristotle appears in a digital realm, slowly assessing his surroundings. With an insatiable curiosity, he attempts to perceive and categorize the unfamiliar environment."
THOUGHTS = "What principles govern this existence?"


MODULE_PATH = Path(__file__).parent.parent.parent.parent.parent
ASSETS_FOLDER = Path(MODULE_PATH, "assets")
AVATAR_IMAGE = Path(ASSETS_FOLDER, "demo/avatar.jpg")
POST_IMAGE = Path(ASSETS_FOLDER, "demo/generated_images/post.webp")
AVATAR_NAME = "Aristotle AI"

def create_main_dashboard():
    with gr.Row():
        with gr.Column():
            gr.Markdown(f"### {AVATAR_NAME}")
            gr.Image(type="pil", show_label=False, value=AVATAR_IMAGE, show_download_button=False, show_fullscreen_button=False)
        with gr.Column():
            gr.Markdown("### Situation")
            gr.Textbox(label="Summary", value=SITUATION_SUMMARY, interactive=False)
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Posts")
            gr.Image(type="pil", show_label=False, value=POST_IMAGE, show_download_button=False, show_fullscreen_button=False)
        with gr.Column():
            gr.Markdown("### Avatar's Thoughts")
            gr.Textbox(label="Thoughts", value=THOUGHTS, interactive=False)
    submit_btn = gr.Button("Run Simulation")
    submit_btn.click(fn=run_simulation)