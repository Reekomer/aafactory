import uuid
from loguru import logger
from tinydb import TinyDB
from PIL import Image
from pathlib import Path
from autonomus_social_media_avatar.configuration import DB_PATH, AVATAR_IMAGES_PATH


AVATAR_TABLE_NAME = "avatar"

def update_avatar_infos(name: str, personality: str, background_knowledge: str, avatar_image: Image.Image, voice_model: str, voice_id: str) -> None:
    """
    Update the avatar infos in the database.
    """
    db = TinyDB(DB_PATH)
    if AVATAR_TABLE_NAME in db.tables():
        db.drop_table(AVATAR_TABLE_NAME)
    table = db.table(AVATAR_TABLE_NAME)
    avatar_image_path = _save_avatar_image(avatar_image, AVATAR_IMAGES_PATH)
    table.insert({"name": name, "personality": personality, "background_knowledge": background_knowledge, "avatar_image_path": avatar_image_path, "voice_model": voice_model, "voice_id": voice_id})
    logger.success(f"Avatar infos updated: {name}, {personality}, {background_knowledge}, {avatar_image_path}")


def _save_avatar_image(avatar_image: Image.Image, avatar_image_folder: Path) -> str:
    """
    Save the avatar image to the avatar image path.
    """
    avatar_image_path = avatar_image_folder / f"{uuid.uuid4()}.png"
    avatar_image.save(avatar_image_path)
    return avatar_image_path.as_posix()

def load_avatar_infos() -> tuple[str, str, str, Image.Image]:
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
            avatar_info.get("avatar_image_path", None),
            avatar_info.get("voice_model", "elevenlabs"),
            avatar_info.get("voice_id", "")
        )
    return "", "", "", None, "", ""