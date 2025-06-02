from fastapi import FastAPI, Query
from db import query
from typing import List

app = FastAPI(title="PalChat API")

@app.get("/messages")
def get_all_messages(limit: int = 50, offset: int = 0):
    rows = query(
        "SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT %s OFFSET %s",
        (limit, offset),
    )
    return rows

@app.get("/messages/by_user")
def get_by_user(username: str):
    rows = query("SELECT * FROM chat_messages WHERE username = %s", (username,))
    return rows

@app.get("/messages/by_suffix")
def get_by_suffix(code: str):
    rows = query("SELECT * FROM chat_messages WHERE profile_code = %s", (code,))
    return rows

@app.get("/messages/by_channel")
def get_by_channel(channel: str):
    rows = query("SELECT * FROM chat_messages WHERE channel = %s", (channel,))
    return rows

