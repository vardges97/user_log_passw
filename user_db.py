
import json
from datetime import datetime
from passlib.context import CryptContext


pwd_context = CryptContext(schemes="sha256_crypt")

def _initialize_user_file(users: dict):
    try:
        with open("users.json", "w") as file:
            json.dump(users, file, indent=2)
    except FileExistsError:
        pass

def _write_users_db(users):
    users_file = "users.json"
    with open(users_file, "w") as file:
        json.dump(users, file, indent=2)

def _read_user_db()-> dict:
    try:
        with open("users.json") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def hash_password(password: str)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

def log_activity(event_type: str, username: str, status: str = None):
    try:
        with open("logs.json", "r") as file:
            logs = json.loads(file.read() or "[]")
    except FileNotFoundError:
        logs = []

    log_entry = {
        "event": event_type,
        "username": username,
        "timestamp": datetime.now().isoformat()
    }
    if status:
        log_entry["status"] = status
    logs.append(log_entry)

    with open("logs.json", "w") as file:
        json.dump(logs, file, indent=2)

def register_user(username: str, password: str):
    db = _read_user_db()
    if username in db:
        return False
    db[username] = {"username": username, "password": hash_password(password)}
    _initialize_user_file(db)
    _write_users_db(db)
    return True

def authenticate_user(username: str, password: str)-> bool:
    db = _read_user_db()
    user = db.get(username)
    if not user or not verify_password(password, user["password"]):
        log_activity("login", username, status="failure to authenticate")
        return False

    log_activity("login", username, status="success")
    return True