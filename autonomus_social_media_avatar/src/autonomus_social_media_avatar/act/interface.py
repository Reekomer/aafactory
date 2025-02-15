import gradio as gr

def create_act_interface():
    with gr.Blocks() as act:
        gr.Markdown("Act")
        gr.Textbox(label="Message")
        gr.Button("Send")
    return act