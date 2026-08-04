from _api.core import sio


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
