import asyncio
from pathlib import Path
from autonomus_social_media_avatar.simulator.avatar.avatar_simulation import run_acting
from autonomus_social_media_avatar.simulator.environment.environment_simulation import create_news_feed, create_social_media_posts, run_environment_simulation_step
from autonomus_social_media_avatar.simulator.narrator.narrator_simulation import run_narration
from autonomus_social_media_avatar.simulator.database.simulation_db import create_simulation_db
from loguru import logger
from tqdm import tqdm

NUMBER_OF_STEPS = 2
ROOT_DIR = Path(__file__).parent.parent.parent
DB_PATH = ROOT_DIR / "databases" / "aristotle_avatar_simulation_db.json"

@profile
async def run_simulation():
    db_path = await create_simulation_db(DB_PATH)
    for steps in tqdm(range(NUMBER_OF_STEPS), desc="Running simulation"):
        if steps != 0:
            social_media_posts = await create_social_media_posts(db_path)
            news_feed = await create_news_feed(db_path)
        environment_simulation_step = await run_environment_simulation_step(db_path)
        narration = await run_narration(db_path, environment_simulation_step)
        acting = await run_acting(db_path, narration)
        # avatar_post_replies = create_avatar_post_replies(db_path, acting)
        logger.info(f"Step {steps}")

if __name__ == "__main__":
    asyncio.run(run_simulation())
