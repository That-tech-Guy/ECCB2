# storage.py
import json, os, re, time
from typing import List, Dict, Any

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

EMAIL_RE = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)

ECCU_COUNTRIES = [
    "Anguilla", "Antigua & Barbuda", "Dominica", "Grenada",
    "Montserrat", "St. Kitts & Nevis", "St. Lucia",
    "St. Vincent & the Grenadines",
]

def valid_email(addr: str) -> bool:
    return bool(EMAIL_RE.match(addr or ""))

def _safe_name(email: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", email.strip().lower())

def user_path(email: str) -> str:
    return os.path.join(DATA_DIR, f"user_{_safe_name(email)}.json")

def save_user_profile(name: str, country: str, email: str):
    payload = {
        "name": name.strip(),
        "country": country.strip(),
        "email": email.strip().lower(),
        "created_at": int(time.time()),
    }
    with open(user_path(email), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return payload

def save_chat_log(email: str, messages: List[Dict[str, Any]]):
    path = os.path.join(DATA_DIR, f"chat_{_safe_name(email)}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    return path
