# auth.py
import bcrypt
from database import db
from models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())

def register_user(username: str, password: str, role: str = "it_analyst"):
    password_hash = hash_password(password)
    db.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )

def authenticate(username: str, password: str):
    user = User.get_by_username(username)
    if not user:
        return None
    if verify_password(password, user.password_hash):
        return user
    return None

if __name__ == "__main__":
    u = input("Username: ")
    p = input("Password: ")
    register_user(u, p)
    print("User registered.")
