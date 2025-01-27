import json
from tinydb import TinyDB
from pathlib import Path

MODULE_PATH = Path(__file__).parent.parent.parent.parent.parent
START_ENVIRONMENT_PATH = MODULE_PATH / "datasets" / "start_environment_v1.json"


async def save_single_to_db(db_path: Path, data: dict, table_name: str) -> None:
    db = TinyDB(db_path)
    table = db.table(table_name)
    table.insert(data)
    db.close()

async def create_simulation_db(db_path: Path) -> Path:
    if not db_path.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(db_path, "w") as f:
            f.write("{}")
    start_environment = _load_start_environment()
    await _save_data_to_specific_table(db_path, start_environment)
    return db_path


def _load_start_environment():
    with open(START_ENVIRONMENT_PATH, "r") as f:
        environment_data = json.load(f)
    return environment_data


async def _save_data_to_specific_table(db_path: Path, start_environment: dict) -> None:
    for table_name, data in start_environment.items():
        if isinstance(data, list):
            await save_multiple_to_db(db_path, data, table_name)


async def save_multiple_to_db(db_path: Path, data: list[dict], table_name: str) -> None:
    db = TinyDB(db_path)
    table = db.table(table_name)
    table.insert_multiple(data)
    db.close()
