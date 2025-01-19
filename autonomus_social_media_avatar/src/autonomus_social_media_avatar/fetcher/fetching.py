from autonomus_social_media_avatar.fetcher.environment_objects import AvatarEnvironment
from openai import BaseModel
from openai import OpenAI
import os
import asyncio
from typing import Callable, List, Tuple, Any

client = OpenAI(api_key=os.getenv("EXPERIMENT_OPENAI_API_KEY"))

def run_fetcher(simulation=False) -> AvatarEnvironment:
    if simulation:
        _fetch_simulation_data()
        return AvatarEnvironment()
    return _fetch_live_data()


def _fetch_simulation_data() -> AvatarEnvironment:
    return AvatarEnvironment()


def _fetch_live_data() -> AvatarEnvironment:
    return AvatarEnvironment()


async def send_request_to_open_ai(prompt: str, response_format: BaseModel) -> BaseModel:
    response = client.beta.chat.completions.parse(
        model="gpt-4o", # gpt-4o-mini
        messages=[{"role": "user", "content": prompt}],
        response_format=response_format,
        temperature=1.0,
        top_p=1.0,
    )
    return response.choices[0].message.parsed


async def asyncio_concurrency_with_semaphore(
    task: Callable,
    batch_task_args: List[Tuple],
    max_concurrent_tasks: int = 20,
) -> List[Any]:
    """Apply concurrency on provided task using asyncio and semaphore.
    If max_concurrent_tasks is not None, semaphore will be used to limit
    the number of tasks that can be processed simultaniously."""
    semaphore = (
        asyncio.Semaphore(max_concurrent_tasks) if max_concurrent_tasks else None
    )

    tasks = [
        _run_task_with_concurrency(task, task_arguments, semaphore)
        for task_arguments in batch_task_args
    ]
    results = await asyncio.gather(*tasks)
    return results


# pylint: disable=missing-function-docstring
async def _run_task_with_concurrency(
    task: Callable,
    task_arguments: Tuple,
    semaphore: asyncio.Semaphore | None,
) -> Any:
    if semaphore:
        async with semaphore:
            return await task(*task_arguments)
    else:
        return await task(*task_arguments)
