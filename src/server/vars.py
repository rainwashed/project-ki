import socketio

sio = socketio.AsyncServer(async_mode="aiohttp", cors_allowed_origins="*", ping_timeout=60)