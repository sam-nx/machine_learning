from _api.core import sio
from _api.store import t_players, t_cells
from _api.sh_methods import cell_key


@sio.event
async def move(sid, data):
    x, y = data['x'], data['y']
    t_players[sid] = {'x': x, 'y': y}
    t_cells[cell_key(x, y)] = sid

    await sio.emit('player_move', {'id': sid, 'x': x, 'y': y}, skip_sid=sid)
    await sio.emit('cell_claimed', {'x': x, 'y': y,
                                    'ownerId': sid}, skip_sid=sid)
