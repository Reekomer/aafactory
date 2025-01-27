from autonomus_social_media_avatar.configuration import DB_PATH
import gradio as gr
from loguru import logger
import pandas as pd
from tinydb import TinyDB

def create_avatar_database_explorer():
    gr.Markdown("### Database Explorer")
    select_table = gr.Dropdown(label="Select Table", choices=['friends_list', 'enemy_list', 'settings', 'avatar_latest_narrations', 'latest_posts', 'latest_news', 'avatar_latest_acting'], value="avatar_latest_acting")
    data_table = gr.Dataframe(interactive=True)
    submit_btn = gr.Button("Load Data")
    submit_btn.click(_load_data, inputs=[select_table], outputs=[data_table])


def _load_data(select_table: str) -> list[dict]:
    logger.info("Loading Data ...")
    db = TinyDB(DB_PATH)
    data = db.table(select_table).all()
    logger.success("Data loaded")
    return pd.DataFrame(data)
