import random
from _api.core import sio
from _api.store import t_players, t_cells
from _api.sh_methods import cell_key


@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

    x, y = random.randint(0, 9), random.randint(0, 9)
    t_players[sid] = {'x': x, 'y': y}
    t_cells[cell_key(x, y)] = sid

    await sio.emit('players_state', t_players, to=sid)
    await sio.emit('cells_state', t_cells, to=sid)

    await sio.emit('player_joined', {'id': sid, 'x': x, 'y': y}, skip_sid=sid)
    await sio.emit('cell_claimed', {'x': x, 'y': y,
                                    'ownerId': sid}, skip_sid=sid)
