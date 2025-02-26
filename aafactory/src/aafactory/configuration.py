from pathlib import Path
import warnings

warnings.filterwarnings('ignore', message='Video does not have browser-compatible container or codec.*')
warnings.filterwarnings('ignore', message='You have not specified a value for the `type` parameter.*')

ROOT_DIR = Path(__file__).parent.parent.parent
DB_PATH = ROOT_DIR / "databases" / "aristotle_avatar_simulation_db.json"
VOICE_PATH = ROOT_DIR / "assets/generated_voice/"
WORKFLOW_FOLDER = ROOT_DIR / "workflows"
DEFAULT_AVATAR_IMAGE_PATH = ROOT_DIR / "assets/demo/avatar.jpg"
AVATAR_IMAGES_PATH = ROOT_DIR / "assets/avatar_images"

SETTINGS_TABLE_NAME = "settings"
AVATAR_TABLE_NAME = "avatar"
