import gradio as gr

def create_react_interface():
    with gr.Blocks() as react:
        gr.Markdown("React")
        gr.Textbox(label="Message")
        gr.Button("Send")
    return react