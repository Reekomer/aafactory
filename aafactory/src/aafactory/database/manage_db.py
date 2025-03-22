import uuid
import numpy as np
import gradio as gr
import soundfile as sf
from aafactory.schemas import Settings
from loguru import logger
from tinydb import TinyDB
from PIL import Image
from pathlib import Path
from aafactory.configuration import AVATAR_TABLE_NAME, DB_PATH, AVATAR_IMAGES_PATH, DEFAULT_VOICE_RECORDING_PATH, SETTINGS_TABLE_NAME, AVATAR_VOICE_RECORDINGS_PATH


def update_avatar_infos(name: str, personality: str, background_knowledge: str, avatar_image: Image.Image, voice_model: str, voice_id: str, voice_recording: bytes, audio_transcript: str, voice_language: str) -> None:
    """
    Update the avatar infos in the database.
    """
    db = TinyDB(DB_PATH)
    voice_recording_file_path = _save_voice_recording(voice_recording)
    if AVATAR_TABLE_NAME in db.tables():
        db.drop_table(AVATAR_TABLE_NAME)
    table = db.table(AVATAR_TABLE_NAME)
    avatar_image_path = _save_avatar_image(avatar_image, AVATAR_IMAGES_PATH)
    avatar_infos = {"name": name, "personality": personality, "background_knowledge": background_knowledge, "avatar_image_path": avatar_image_path, "voice_model": voice_model, "voice_id": voice_id, "voice_language": voice_language, "voice_recording_path": voice_recording_file_path, "audio_transcript": audio_transcript}
    table.insert(avatar_infos)
    logger.success(f"Avatar infos updated: {avatar_infos}")
    gr.Info("Avatar infos updated",)


def _save_voice_recording(voice_recording: tuple[int, np.ndarray]) -> str:
    """
    Save the voice recording to the voice recording path.
    """
    voice_recording_file_path = AVATAR_VOICE_RECORDINGS_PATH / f"{uuid.uuid4()}.wav"
    sf.write(voice_recording_file_path, voice_recording[1], voice_recording[0])
    return voice_recording_file_path.as_posix()


def _save_avatar_image(avatar_image: Image.Image, avatar_image_folder: Path) -> str:
    """
    Save the avatar image to the avatar image path.
    """
    avatar_image_folder.mkdir(parents=True, exist_ok=True)
    avatar_image_path = avatar_image_folder / f"{uuid.uuid4()}.png"
    avatar_image.save(avatar_image_path)
    return avatar_image_path.as_posix()

def load_avatar_infos() -> tuple[str, str, str, Image.Image, str, str, str, str]:
    """
    Load the avatar infos from the database.
    """
    db = TinyDB(DB_PATH)
    table = db.table(AVATAR_TABLE_NAME)
    avatar_info = table.get(doc_id=1)  # Changed from 0 to 1 since TinyDB starts at 1
    if avatar_info:
        return (
            avatar_info.get("name", ""),
            avatar_info.get("personality", ""),
            avatar_info.get("background_knowledge", ""),
            avatar_info.get("avatar_image_path", ""),
            avatar_info.get("voice_model", ""),
            avatar_info.get("voice_id", ""),
            avatar_info.get("voice_recording_path", DEFAULT_VOICE_RECORDING_PATH.as_posix()),
            avatar_info.get("audio_transcript", ""),
            avatar_info.get("voice_language", "")
        )
    return "", "", "", "", "", "", "", "", ""


def get_settings() -> Settings:
    """
    Get the settings from the database.
    """
    db = TinyDB(DB_PATH)
    table = db.table(SETTINGS_TABLE_NAME)
    return Settings(**table.get(doc_id=1))