from pathlib import Path

# Create test paths that are separate from production
TEST_DIR = Path(__file__).parent / "test_data"
TEST_DB_PATH = TEST_DIR / "test_avatar_db.json"
TEST_AVATAR_IMAGE_PATH = TEST_DIR / "test_avatar.png"

# Create test directories if they don't exist
TEST_DIR.mkdir(parents=True, exist_ok=True)