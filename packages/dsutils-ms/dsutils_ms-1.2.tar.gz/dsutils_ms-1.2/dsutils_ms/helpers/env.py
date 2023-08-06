from os import getenv
from dotenv.main import load_dotenv
from os.path import exists
import json
from pathlib import Path
from dsutils_ms.helpers.log import log_title


def load_env(path_finder: str = "./"):
    PATH = path_finder

    tries = 0
    while True:
        tries = tries + 1
        if exists(PATH + ".env"):
            load_dotenv(Path(PATH + ".env"))
            log_title("Loading .env file")
            break
        if exists(PATH + ".gitignore"):
            break
        PATH = "../" + PATH
        if tries > 10:
            raise Exception(".env file not found after 10 tries")

    if not exists(PATH + ".env"):
        raise Exception(".env file not found")


def get_credential(key: str) -> str:
    load_env()

    data = getenv(key)

    if data is None:
        raise Exception(f"Environment variable {key} not found")

    JSON_CREDENTIALS = ["GOOGLE_SERVICE_ACCOUNT"]
    if key in JSON_CREDENTIALS:
        data = data.replace("\\\\n", "\\n")
        data = json.loads(data)

    return data
