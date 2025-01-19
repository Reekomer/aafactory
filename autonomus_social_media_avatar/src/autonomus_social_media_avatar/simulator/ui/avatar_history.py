import gradio as gr

def create_avatar_history():
    gr.Markdown("### History")
    history_table = gr.Dataframe(headers=["Date", "Situation", "Thoughts", "Post Image"], interactive=False)
    submit_btn = gr.Button("Load History")
    # submit_btn.click(load_history, history_table)