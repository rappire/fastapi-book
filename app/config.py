import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def get_secret(key, json_path: str = str(BASE_DIR / "secrets.json")):
    with open(json_path) as file:
        secrets = json.loads(file.read())
        try:
            return secrets[key]
        except:
            raise EnvironmentError(f"There is not {key} in file")


MONGO_DB_NAME = get_secret("MONGO_DB_NAME")
MONGO_URL = get_secret("MONGO_URL")
NAVER_API_ID = get_secret("NAVER_API_ID")
NAVER_API_SECRET = get_secret("NAVER_API_SECRET")
