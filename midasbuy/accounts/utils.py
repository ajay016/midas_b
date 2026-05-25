import json
import os
import shutil
from pathlib import Path
from typing import Optional


def get_midasbuy_session_dir(base_dir, account_id: int) -> str:
    return os.path.join(base_dir, "midasbuy_sessions", f"account_{account_id}")


def ensure_clean_session_dir(session_dir: str) -> Path:
    path = Path(session_dir)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_session_dir(session_dir: str) -> Path:
    path = Path(session_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json_file(file_path: str, data) -> str:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return file_path


def save_text_file(file_path: str, value: str) -> str:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(value)
    return file_path


def load_json_file(file_path: Optional[str]):
    if not file_path or not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text_file(file_path: Optional[str]) -> Optional[str]:
    if not file_path or not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def file_exists(file_path: Optional[str]) -> bool:
    return bool(file_path and os.path.exists(file_path))


def get_cookie_file_path(session_dir: str) -> str:
    return os.path.join(session_dir, "cookies.json")


def get_storage_state_file_path(session_dir: str) -> str:
    return os.path.join(session_dir, "storage_state.json")


def get_token_file_path(session_dir: str) -> str:
    return os.path.join(session_dir, "access_token.txt")


def get_meta_file_path(session_dir: str) -> str:
    return os.path.join(session_dir, "meta.json")


def get_screenshot_file_path(session_dir: str, name: str = "login_result.png") -> str:
    return os.path.join(session_dir, name)


def get_html_snapshot_file_path(session_dir: str, name: str = "last_page.html") -> str:
    return os.path.join(session_dir, name)


def get_xmidas_token_file_path(session_dir: str) -> str:
    return os.path.join(session_dir, "xmidas_token.txt")


def get_session_storage_file_path(session_dir: str) -> str:
    return os.path.join(session_dir, "session_storage.json")


def get_account_token(session_dir: str) -> str:
    token_path = get_token_file_path(session_dir)
    token = load_text_file(token_path)
    return token if token else ""


def get_account_ctoken_from_storage(session_dir: str) -> str:
    storage_state_path = get_storage_state_file_path(session_dir)
    storage_state = load_json_file(storage_state_path)

    if storage_state:
        for cookie in storage_state.get("cookies", []):
            if cookie.get("name") == "ctoken":
                return cookie.get("value", "")
            if "token" in cookie.get("name", "").lower():
                return cookie.get("value", "")

    return ""


def get_account_auth_data(session_dir: str) -> dict:
    token = get_account_token(session_dir)
    ctoken = get_account_ctoken_from_storage(session_dir)

    meta_path = get_meta_file_path(session_dir)
    meta_data = load_json_file(meta_path)

    return {
        "token": token,
        "ctoken": ctoken,
        "ctoken_ver": "1.0.1",
        "session_dir": session_dir,
        "has_valid_session": bool(token or ctoken),
        "meta": meta_data,
    }


def get_account_cookies(session_dir: str) -> list:
    cookie_path = get_cookie_file_path(session_dir)
    cookies = load_json_file(cookie_path)
    return cookies if cookies else []


def is_account_session_valid(session_dir: str) -> bool:
    required_files = [
        get_storage_state_file_path(session_dir),
        get_cookie_file_path(session_dir),
        get_meta_file_path(session_dir),
    ]

    for file_path in required_files:
        if not file_exists(file_path):
            return False

    auth_data = get_account_auth_data(session_dir)
    return auth_data["has_valid_session"]
