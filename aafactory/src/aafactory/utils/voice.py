import json
from pathlib import Path
import uuid
from comfyui.video import QueueHistory, queue_task, upload_files_to_comfyui_server
from configuration import DB_PATH, TEXT_TO_SPEECH_WITH_ZONOS_WORKFLOW_PATH, GENERATED_VOICE_PATH
from database.manage_db import get_settings
from schemas import Settings
from loguru import logger
import requests
from tinydb import TinyDB

async def send_request_to_elevenlabs(prompt: str, voice_id: str) -> Path:
    # Get API key from settings
    db = TinyDB(DB_PATH)
    settings = db.table("settings").all()[-1]
    api_key = settings["elevenlabs_api_key"]
    voice_id = voice_id
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": prompt,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Save the audio file
        output_path = GENERATED_VOICE_PATH / f"{uuid.uuid4().hex}.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return output_path
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to ElevenLabs: {e}")
        raise e


async def send_request_to_zonos(text_response: str, voice_language: str, voice_recording_path: str, audio_transcript: str) -> Path:
    """
    Send a request to the server to generate a video.
    """
    settings = get_settings()
    voice_recording_path = Path(voice_recording_path)
    upload_files_to_comfyui_server([voice_recording_path])
    workflow = _create_text_to_speech_with_zonos_workflow(text_response, voice_language, voice_recording_path, audio_transcript)
    queue_history = await queue_task(workflow, settings)
    audio_url = _get_audio_url(settings, queue_history)
    output_path = _save_audio_to_file(audio_url)
    return output_path


def _create_text_to_speech_with_zonos_workflow(text_response: str, voice_language: str, voice_recording_path: Path, audio_transcript: str) -> dict:
    """
    Create a workflow for the text to speech with Zonos.
    """
    with open(TEXT_TO_SPEECH_WITH_ZONOS_WORKFLOW_PATH, "r") as f:
        workflow = json.load(f)
    workflow["12"]["inputs"]["audio"] = voice_recording_path.name
    workflow["24"]["inputs"]["speech"] = text_response
    workflow["24"]["inputs"]["language"] = voice_language
    workflow["24"]["inputs"]["sample_text"] = audio_transcript
    return {"prompt": workflow}


def _get_audio_url(settings: Settings, queue_history: QueueHistory) -> str:
    """
    Get the audio URL from the history response.
    """
    output_info = queue_history.response.get(queue_history.prompt_id, {}).get('outputs', {}).get('13', {}).get('audio', [{}])[0]
    filename = output_info.get('filename', 'unknown.mp3')
    output_url = f"{settings.comfy_server_url}/api/view?filename={filename}&subfolder=&type=temp"
    logger.success(f"Output URL: {output_url}")
    return output_url


def _save_audio_to_file(audio_url: str) -> Path:
    """
    Save the audio to a file.
    """
    output_path = GENERATED_VOICE_PATH / f"{uuid.uuid4().hex}.mp3"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(audio_url)
    with open(output_path, "wb") as f:
        f.write(response.content)
    logger.success(f"Audio saved to {output_path}")
    return output_path