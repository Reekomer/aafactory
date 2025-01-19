import os
from pathlib import Path
from autonomus_social_media_avatar.fetcher.environment_objects import Acting
from autonomus_social_media_avatar.fetcher.environment_objects import Narration
from autonomus_social_media_avatar.fetcher.fetching import asyncio_concurrency_with_semaphore, send_request_to_open_ai
from autonomus_social_media_avatar.prompts import AVATAR_DESCRIPTION
from autonomus_social_media_avatar.simulator.database.simulation_db import save_multiple_to_db, save_single_to_db
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()   

client = OpenAI(api_key=os.getenv("EXPERIMENT_OPENAI_API_KEY"))

TABLE_NAME = "avatar_latest_acting"
PROMPT = """
Based on the narration data, create an acting for the avatar.
All the values should be between 0 and 1.

Avatar description:
{avatar_description}

Narration data:
{narration_data}
"""

async def run_acting(db_path: Path, narration: Narration) -> Acting:
    prompt = PROMPT.format(avatar_description=AVATAR_DESCRIPTION, narration_data=narration)
    request_args = [
        (prompt, Acting)
    ]
    acting = await asyncio_concurrency_with_semaphore(
        send_request_to_open_ai,
        request_args,
        None,
    )
    data_to_save = [acting.model_dump() for acting in acting]
    await save_multiple_to_db(db_path, data_to_save, TABLE_NAME)
    return acting