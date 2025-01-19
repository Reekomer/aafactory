import os
from pathlib import Path

from autonomus_social_media_avatar.fetcher.fetching import asyncio_concurrency_with_semaphore, send_request_to_open_ai
from autonomus_social_media_avatar.prompts import NEWS_PROMPT, SOCIAL_MEDIA_PROMPT
from autonomus_social_media_avatar.simulator.database.simulation_db import save_multiple_to_db, save_single_to_db
from dotenv import load_dotenv
from openai import OpenAI
from tinydb import TinyDB
from autonomus_social_media_avatar.fetcher.environment_objects import AvatarEnvironment, News, Post

load_dotenv()   

client = OpenAI(api_key=os.getenv("EXPERIMENT_OPENAI_API_KEY"))

SOCIAL_MEDIA_TABLE_NAME = "latest_posts"
NEWS_TABLE_NAME = "latest_news"

PROMPT = """
Based on the environment data, create a narration for the avatar.
All the values should be between 0 and 1.

Avatar description:
{avatar_description}

Environment data:
{environment_data}
"""

async def create_social_media_posts(db_path: Path) -> list[Post]:
    request_args = [
        (SOCIAL_MEDIA_PROMPT, Post)
        for _ in range(3)
    ]
    posts = await asyncio_concurrency_with_semaphore(
        send_request_to_open_ai,
        request_args,
        None,
    )
    data_to_save = [post.model_dump() for post in posts]
    await save_multiple_to_db(db_path, data_to_save, SOCIAL_MEDIA_TABLE_NAME)
    return posts


async def create_news_feed(db_path: Path) -> list[News]:
    request_args = [
        (NEWS_PROMPT, News)
        for _ in range(3)
    ]
    news = await asyncio_concurrency_with_semaphore(
        send_request_to_open_ai,
        request_args,
        None,
    )
    data_to_save = [news.model_dump() for news in news]
    await save_multiple_to_db(db_path, data_to_save, NEWS_TABLE_NAME)
    return news


@profile
async def run_environment_simulation_step(db_path: Path) -> AvatarEnvironment:
    environment_data = await _get_latest_environment_data(db_path)
    environment_data["storyline_phase"] = "Introduction"
    return AvatarEnvironment(**environment_data)


@profile
async def _get_latest_environment_data(db_path: Path) -> dict:
    # Open DB connection once
    db = TinyDB(db_path)
    environment_data = {}
    
    # Get all table names first to avoid repeated calls
    tables = db.tables()
    
    # Use dict comprehension for better performance
    environment_data = {
        table_name: [db.table(table_name).all()[-1]]
        for table_name in tables
    }
    
    # Close the connection explicitly
    db.close()
    
    return environment_data
