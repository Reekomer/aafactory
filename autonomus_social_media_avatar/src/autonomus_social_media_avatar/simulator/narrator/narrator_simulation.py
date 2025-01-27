import os
from pathlib import Path
from autonomus_social_media_avatar.fetcher.environment_objects import AvatarEnvironment
from autonomus_social_media_avatar.fetcher.environment_objects import Narration
from autonomus_social_media_avatar.fetcher.fetching import asyncio_concurrency_with_semaphore, send_request_to_open_ai
from autonomus_social_media_avatar.prompts import AVATAR_DESCRIPTION
from autonomus_social_media_avatar.simulator.database.simulation_db import save_multiple_to_db, save_single_to_db
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()   

client = OpenAI(api_key=os.getenv("EXPERIMENT_OPENAI_API_KEY"))

TABLE_NAME = "avatar_latest_narrations"
PROMPT = """
Based on the environment data, create a narration for the avatar.
All the values should be between 0 and 1.

Avatar description:
{avatar_description}

Environment data:
{environment_data}
"""


async def run_narration(db_path: Path, environment_data: AvatarEnvironment) -> Narration:
    prompt = PROMPT.format(avatar_description=AVATAR_DESCRIPTION, environment_data=environment_data)
    request_args = [
        (prompt, Narration)
    ]
    narrations = await asyncio_concurrency_with_semaphore(
        send_request_to_open_ai,
        request_args,
        None,
    )
    data_to_save = [narration.model_dump() for narration in narrations]
    # _manage_skills
    # _manage_inventory
    await save_multiple_to_db(db_path, data_to_save, TABLE_NAME)
    return narrations[0]
