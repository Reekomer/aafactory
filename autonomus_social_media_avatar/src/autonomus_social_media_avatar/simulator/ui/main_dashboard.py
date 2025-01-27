from autonomus_social_media_avatar.configuration import DB_PATH
from autonomus_social_media_avatar.simulation import run_simulation
from autonomus_social_media_avatar.simulator.database.simulation_db import create_simulation_db
import gradio as gr
from pathlib import Path

SITUATION_SUMMARY = "Aristotle appears in a digital realm, slowly assessing his surroundings. With an insatiable curiosity, he attempts to perceive and categorize the unfamiliar environment."
THOUGHTS = "What principles govern this existence?"


MODULE_PATH = Path(__file__).parent.parent.parent.parent.parent
ASSETS_FOLDER = Path(MODULE_PATH, "assets")
AVATAR_IMAGE = Path(ASSETS_FOLDER, "demo/avatar.jpg")
POST_IMAGE = Path(ASSETS_FOLDER, "demo/generated_images/post.webp")
AVATAR_NAME = "Aristotle AI"

async def create_main_dashboard():
    if not DB_PATH.exists():
        await create_simulation_db(DB_PATH)
    with gr.Row():
        with gr.Column():
            gr.Markdown(f"### {AVATAR_NAME}")
            gr.Image(type="pil", show_label=False, value=AVATAR_IMAGE, show_download_button=False, show_fullscreen_button=False)
        with gr.Column():
            gr.Markdown("### Situation")
            narration = gr.Textbox(label="Narration", value=SITUATION_SUMMARY, interactive=False)
            acting = gr.TextArea(label="Thoughts", value=THOUGHTS, interactive=False)
            posts = gr.Image(label="Illustration", type="pil", value=POST_IMAGE, show_download_button=False, show_fullscreen_button=False)
            avatar_voice = gr.Audio(label="Avatar Voice", type="filepath")
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Social Media")
            social_media = gr.TextArea(label="Social Media", show_label=False, value="", interactive=False)
        with gr.Column():
            gr.Markdown("### News Feed")
            news_feed = gr.TextArea(label="News Feed", show_label=False, value="", interactive=False)

    submit_btn = gr.Button("Run Simulation")
    submit_btn.click(fn=run_simulation, show_progress="full", outputs=[narration, acting, social_media, news_feed, avatar_voice])