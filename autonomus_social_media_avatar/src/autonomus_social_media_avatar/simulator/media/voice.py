from pathlib import Path
import uuid
from autonomus_social_media_avatar.configuration import DB_PATH, VOICE_PATH
from autonomus_social_media_avatar.fetcher.environment_objects import Acting
from autonomus_social_media_avatar.fetcher.fetching import asyncio_concurrency_with_semaphore
import requests
from tinydb import TinyDB

async def run_avatar_voice(acting: Acting) -> Path:
    prompt = " ".join(acting.thoughts)
    request_args = [
        (prompt,)
    ]
    avatar_voice = await asyncio_concurrency_with_semaphore(
        send_request_to_elevenlabs,
        request_args,
        None,
    )
    return avatar_voice[0]


async def send_request_to_elevenlabs(prompt: str) -> Path:
    # Get API key from settings
    db = TinyDB(DB_PATH)
    settings = db.table("settings").all()[-1]
    api_key = settings["elevenlabs_api_key"]
    voice_id = settings["voice_id"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": prompt,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Save the audio file
        output_path = VOICE_PATH / f"{uuid.uuid4().hex}.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to ElevenLabs: {e}")
        raise