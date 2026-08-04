from _api.core import sio
from _api.store import t_players


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    t_players.pop(sid, None)
    await sio.emit('player_left', {'id': sid})
