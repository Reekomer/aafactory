import gradio as gr

def create_settings():
    gr.Markdown("### Settings")
    comfyui_server_url = gr.Textbox(label="ComfyUI Server URL", value="http://localhost:8188", interactive=True)
    openai_api_key = gr.Textbox(label="OpenAI API Key", value="", interactive=True)
    elevenlabs_api_key = gr.Textbox(label="ElevenLabs API Key", value="", interactive=True)
    submit_btn = gr.Button("Save Settings")