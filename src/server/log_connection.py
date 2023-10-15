import asyncio
from enum import Enum
from time import time as now_time
from server.vars import sio

start = now_time()

class LogTypes(Enum):
    info = 0
    warning = 1
    success = 2
    unknown = 3
    failure = 4

log_icons = {
    LogTypes.info: "ℹ️",
    LogTypes.warning: "⚠️",
    LogTypes.success: "✅",
    LogTypes.unknown: "❓",
    LogTypes.failure: "❌"
}

async def log(module: str, message: str, type: LogTypes = LogTypes.info):
    s: str = f"[{round((now_time() * 1000) - start)}, {log_icons[type]}] - {message} ({module})"

    await sio.emit("log_message", s)
