import asyncio
from pathlib import Path
from autonomus_social_media_avatar.configuration import DB_PATH
from autonomus_social_media_avatar.simulator.avatar.avatar_simulation import run_acting
from autonomus_social_media_avatar.simulator.environment.environment_simulation import create_news_feed, create_social_media_posts, run_environment_simulation_step
from autonomus_social_media_avatar.simulator.media.voice import run_avatar_voice
from autonomus_social_media_avatar.simulator.narrator.narrator_simulation import run_narration
from autonomus_social_media_avatar.simulator.database.simulation_db import create_simulation_db
from autonomus_social_media_avatar.simulator.ui.settings import Settings
from loguru import logger
from tinydb import TinyDB
from tqdm import tqdm

NUMBER_OF_STEPS = 1


async def run_simulation() -> tuple[str, str, str, str]:
    settings = _load_settings()
    if settings.create_new_database:
        db_path = await create_simulation_db(DB_PATH)
    else:
        db_path = DB_PATH
    for steps in tqdm(range(1,NUMBER_OF_STEPS+1), desc="Running simulation"):
        # if steps != 1: # creates a base for the simulation
        social_media_posts = await create_social_media_posts(db_path)
        news_feed = await create_news_feed(db_path)
        environment_simulation_step = await run_environment_simulation_step(db_path)
        narration = await run_narration(db_path, environment_simulation_step)
        acting = await run_acting(db_path, narration)
        avatar_voice = await run_avatar_voice(acting)
        logger.info(f"Step {steps}")
    logger.success("Simulation finished")
    return narration.situation, "\n\n".join(acting.thoughts), "\n\n".join([post.text for post in social_media_posts]), "\n\n".join([news.title for news in news_feed]), avatar_voice


def _load_settings():
    db = TinyDB(DB_PATH)
    settings = db.table("settings").all()[0]
    return Settings(**settings)


if __name__ == "__main__":
    asyncio.run(run_simulation())
