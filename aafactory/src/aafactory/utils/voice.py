from pathlib import Path
import uuid
from aafactory.configuration import DB_PATH, VOICE_PATH
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
        output_path = VOICE_PATH / f"{uuid.uuid4().hex}.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to ElevenLabs: {e}")
        raise