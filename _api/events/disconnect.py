from _api.core import sio


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
