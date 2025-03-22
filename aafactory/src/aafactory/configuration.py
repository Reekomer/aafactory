from pathlib import Path
import warnings

warnings.filterwarnings('ignore', message='Video does not have browser-compatible container or codec.*')
warnings.filterwarnings('ignore', message='You have not specified a value for the `type` parameter.*')

ROOT_DIR = Path(__file__).parent.parent.parent
DB_PATH = ROOT_DIR / "databases" / "avatar_db.json"
GENERATED_VOICE_PATH = ROOT_DIR / "assets/generated_voices/"
GENERATED_VIDEO_PATH = ROOT_DIR / "assets/generated_videos/"
WORKFLOW_FOLDER = ROOT_DIR / "workflows"
DEFAULT_AVATAR_IMAGE_PATH = ROOT_DIR / "assets/demo/avatar.jpg"
DEFAULT_VOICE_RECORDING_PATH = ROOT_DIR / "assets/demo/voice_recording.mp3"
AVATAR_IMAGES_PATH = ROOT_DIR / "assets/avatar_images"

SETTINGS_TABLE_NAME = "settings"
AVATAR_TABLE_NAME = "avatar"
AVATAR_VOICE_RECORDINGS_PATH = ROOT_DIR / "assets/avatar_voice_recordings"

VOICE_MODELS = ["", "elevenlabs", "zonos"]
VOICE_LANGUAGES = [
    'af', 'am', 'an', 'ar', 'as', 'az', 'ba', 'bg', 'bn', 'bpy', 'bs', 'ca', 'cmn',
    'cs', 'cy', 'da', 'de', 'el', 'en-029', 'en-gb', 'en-gb-scotland', 'en-gb-x-gbclan',
    'en-gb-x-gbcwmd', 'en-gb-x-rp', 'en-us', 'eo', 'es', 'es-419', 'et', 'eu', 'fa',
    'fa-latn', 'fi', 'fr-be', 'fr-ch', 'fr-fr', 'ga', 'gd', 'gn', 'grc', 'gu', 'hak',
    'hi', 'hr', 'ht', 'hu', 'hy', 'hyw', 'ia', 'id', 'is', 'it', 'ja', 'jbo', 'ka',
    'kk', 'kl', 'kn', 'ko', 'kok', 'ku', 'ky', 'la', 'lfn', 'lt', 'lv', 'mi', 'mk',
    'ml', 'mr', 'ms', 'mt', 'my', 'nb', 'nci', 'ne', 'nl', 'om', 'or', 'pa', 'pap',
    'pl', 'pt', 'pt-br', 'py', 'quc', 'ro', 'ru', 'ru-lv', 'sd', 'shn', 'si', 'sk',
    'sl', 'sq', 'sr', 'sv', 'sw', 'ta', 'te', 'tn', 'tr', 'tt', 'ur', 'uz', 'vi',
    'vi-vn-x-central', 'vi-vn-x-south', 'yue'
]

TEXT_TO_SPEECH_WITH_ZONOS_WORKFLOW_PATH = ROOT_DIR / "workflows" / "text_to_speech_with_zonos.json"