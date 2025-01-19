from autonomus_social_media_avatar.simulator.ui.avatar_history import create_avatar_history
from autonomus_social_media_avatar.simulator.ui.avatar_profile import create_avatar_profile
from autonomus_social_media_avatar.simulator.ui.main_dashboard import create_main_dashboard
from autonomus_social_media_avatar.simulator.ui.settings import create_settings
import gradio as gr


# Create a Gradio interface
def create_gradio_interface():
    with gr.Blocks() as simulation:
        gr.Markdown("# Simulation")
        with gr.Tabs():
            with gr.Tab(label="Main Dashboard"):  
                create_main_dashboard()
            with gr.Tab(label="Avatar's Profile"):
                create_avatar_profile()
            with gr.Tab(label="History"):
                create_avatar_history()
            with gr.Tab(label="Settings"):
                create_settings()
    return simulation


if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(share=False)
