# models.py
from dataclasses import dataclass
from typing import List, Optional
from database import db

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str

    @staticmethod
    def get_by_username(username: str) -> Optional["User"]:
        rows = db.query("SELECT * FROM users WHERE username = ?", (username,))
        if not rows:
            return None
        r = rows[0]
        return User(r["id"], r["username"], r["password_hash"], r["role"])

@dataclass
class ITTicket:
    id: int = None
    ticket_id: str = None
    requester: str = None
    assigned_to: str = None
    status: str = None
    opened_at: str = None
    resolved_at: str = None
    priority: str = None

    @staticmethod
    def all():
        rows = db.query("SELECT * FROM it_tickets")
        return [ITTicket(**dict(r)) for r in rows]

    @staticmethod
    def create(ticket_id, requester, assigned_to, status, opened_at, resolved_at, priority):
        db.execute(
            """
            INSERT OR IGNORE INTO it_tickets (ticket_id, requester, assigned_to, status, opened_at, resolved_at, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, requester, assigned_to, status, opened_at, resolved_at, priority),
        )

    @staticmethod
    def update(ticket_id, **fields):
        set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
        params = list(fields.values()) + [ticket_id]
        db.execute(f"UPDATE it_tickets SET {set_clause} WHERE ticket_id = ?", params)

    @staticmethod
    def delete(ticket_id):
        db.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
