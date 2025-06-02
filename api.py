from fastapi import FastAPI, Query
from db import query
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI(
    title="MegaPhone API",
    description="Query MegaPhone Data",
    version="1.0.0",
)

DEFAULT_TZ = "Asia/Taipei"


def convert_tz(ts: datetime, tz_name: str) -> str:
    try:
        return ts.astimezone(ZoneInfo(tz_name)).isoformat()
    except Exception:
        return ts.astimezone(ZoneInfo(DEFAULT_TZ)).isoformat()


def apply_timezone(rows: List[dict], tz: str) -> List[dict]:
    for row in rows:
        if "timestamp" in row and row["timestamp"]:
            row["timestamp"] = convert_tz(row["timestamp"], tz)
    return rows


@app.get("/messages")
def get_all_messages(
    limit: int = Query(50, description="Number of messages to return"),
    offset: int = Query(0, description="Offset for pagination"),
    tz: str = Query(
        DEFAULT_TZ, description="Timezone for timestamps", example="Asia/Taipei"
    ),
):
    rows = query(
        "SELECT * FROM chat_messages ORDER BY timestamp DESC LIMIT %s OFFSET %s",
        (limit, offset),
    )
    return apply_timezone(rows, tz)


@app.get("/messages/by_user")
def get_by_user(
    username: str = Query(..., description="Username prefix (e.g. C081RXD00)"),
    tz: str = Query(DEFAULT_TZ, description="Timezone for timestamps", example="UTC"),
):
    rows = query("SELECT * FROM chat_messages WHERE username = %s", (username,))
    return apply_timezone(rows, tz)


@app.get("/messages/by_suffix")
def get_by_suffix(
    code: str = Query(..., description="Profile code suffix (e.g. 9CB2B)"),
    tz: str = Query(
        DEFAULT_TZ, description="Timezone for timestamps", example="Asia/Tokyo"
    ),
):
    rows = query("SELECT * FROM chat_messages WHERE profile_code = %s", (code,))
    return apply_timezone(rows, tz)


@app.get("/messages/by_channel")
def get_by_channel(
    channel: str = Query(..., description="Channel ID (e.g. 1090)"),
    tz: str = Query(
        DEFAULT_TZ, description="Timezone for timestamps", example="Asia/Taipei"
    ),
):
    rows = query("SELECT * FROM chat_messages WHERE channel = %s", (channel,))
    return apply_timezone(rows, tz)
