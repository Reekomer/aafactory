from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
DB_PATH = ROOT_DIR / "databases" / "aristotle_avatar_simulation_db.json"
VOICE_PATH = ROOT_DIR / "assets/generated_voice/"
WORKFLOW_FOLDER = ROOT_DIR / "workflows"
DEFAULT_AVATAR_IMAGE_PATH = ROOT_DIR / "assets/avatar_image.png"
AVATAR_IMAGES_PATH = ROOT_DIR / "assets/avatar_images"
