import json
from pathlib import Path
import time
import uuid
from configuration import GENERATED_VIDEO_PATH, WORKFLOW_FOLDER
from schemas import Settings
from loguru import logger
from pydantic import BaseModel
import requests
import soundfile as sf
from database.manage_db import get_settings


class QueueHistory(BaseModel):
    prompt_id: str
    response: dict


async def send_request_to_generate_video(avatar_image_path: Path, audio_file_path: Path) -> Path:
    """
    Send a request to the server to generate a video.
    """
    settings = get_settings()
    avatar_image_path = Path(avatar_image_path)
    upload_files_to_comfyui_server([avatar_image_path, audio_file_path])
    workflow = _create_workflow(avatar_image_path, audio_file_path)
    queue_history = await queue_task(workflow, settings)
    video_url = _get_video_url(settings, queue_history)
    output_path = _save_video_to_file(video_url)
    return output_path


def upload_files_to_comfyui_server(files: list[Path]) -> None:
    """
    Upload files to the server.
    """
    settings = get_settings()
    comfy_server_url = settings.comfy_server_url
    logger.info(f"Uploading Files to ComfyUI Server at {comfy_server_url} ...")
    for file in files:
        with open(file, "rb") as f:
            to_upload_files = {
                'image': (file.name, f, 'image/' + file.suffix[1:])
            }
            response =requests.post(f"{comfy_server_url}/upload/image", files=to_upload_files)
            if response.status_code == 200:
                logger.success(f"Uploaded {file.name}")
            else:
                logger.error(f"Failed to upload {file.name}. Status code: {response.status_code}")


def _create_workflow(avatar_image_path: Path, audio_file_path: Path) -> dict:
    """
    Create a workflow for the video generation.
    """
    with open(Path(WORKFLOW_FOLDER, "audio_image_to_video_with_sonic.json"), "r") as f:
        workflow = json.load(f)
    workflow["6"]["inputs"]["duration"] = _get_audio_file_duration(audio_file_path)
    workflow["7"]["inputs"]["image"] = avatar_image_path.name
    workflow["9"]["inputs"]["audio"] = audio_file_path.name
    return {"prompt": workflow}


def _get_audio_file_duration(audio_file_path: Path) -> int:
    """
    Get the duration of the audio file.
    """
    info = sf.info(str(audio_file_path))
    return round(info.duration, 2) + 2

async def queue_task(workflow: dict, settings: Settings) -> QueueHistory:
    """
    Queue a task to the server.
    """
    response1 = _queue_prompt(workflow, settings)
    if response1 is None:
        logger.error("Failed to queue the prompt.")
        return

    prompt_id = response1['prompt_id']
    logger.info(f'Prompt ID: {prompt_id}')
    logger.info('-' * 20)
    while True:
        time.sleep(5)
        queue_response = _get_queue(settings.comfy_server_url)
        if queue_response is None:
            continue

        queue_pending = queue_response.get('queue_pending', [])
        queue_running = queue_response.get('queue_running', [])

        # Check position in queue
        for position, item in enumerate(queue_pending):
            if item[1] == prompt_id:
                logger.info(f'Queue running: {len(queue_running)}, Queue pending: {len(queue_pending)}, Workflow is in position {position + 1} in the queue.')

        # Check if the prompt is currently running
        for item in queue_running:
            if item[1] == prompt_id:
                logger.info(f'Queue running: {len(queue_running)}, Queue pending: {len(queue_pending)}, Workflow is currently running.')
                break

        if not any(prompt_id in item for item in queue_pending + queue_running):
            break
    
    response = _get_history(settings.comfy_server_url, prompt_id)
    return QueueHistory(prompt_id=prompt_id, response=response)


def _queue_prompt(prompt: str, settings: Settings):
    data = json.dumps(prompt).encode('utf-8')
    prompt_url = f"{settings.comfy_server_url}/prompt"
    try:
        r = requests.post(prompt_url, data=data, headers={"Content-Type": "application/json"})
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as ex:
        logger.error(f'POST {prompt_url} failed: {ex}')
        return None
    

def _get_queue(url):
    queue_url = f"{url}/queue"
    try:
        r = requests.get(queue_url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as ex:
        print(f'GET {queue_url} failed: {ex}')
        return None
    

def _get_history(url, prompt_id):
    history_url = f"{url}/history/{prompt_id}"
    try:
        r = requests.get(history_url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as ex:
        print(f'GET {history_url} failed: {ex}')
        return None


def _get_video_url(settings: Settings, queue_history: QueueHistory) -> str:
    """
    Get the video URL from the history response.
    """
    output_info = queue_history.response.get(queue_history.prompt_id, {}).get('outputs', {}).get('8', {}).get('gifs', [{}])[0]
    filename = output_info.get('filename', 'unknown.png')
    output_url = f"{settings.comfy_server_url}/api/viewvideo?filename={filename}"
    logger.success(f"Output URL: {output_url}")
    return output_url

def _save_video_to_file(video_url: str) -> Path:
    """
    Save the video to a file.
    """
    output_path = GENERATED_VIDEO_PATH / f"{uuid.uuid4().hex}.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(video_url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    logger.success(f"Video saved to {output_path}")
    return output_path