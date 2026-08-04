from _api.core import sio
from _api.predict import predict_from_buffer


@sio.event
async def predict(sid, data):
    print("Received predict", sid, data)
    s_buffer = data.get('buffer', '')
    if not s_buffer:
        print("No buffer")
        await sio.emit('predict_return', {'error': 'No buffer supplied'},
                       to=sid)
        return
    print("Buffer received")
    await sio.emit('predict_return', {'data': predict_from_buffer(s_buffer)},
                   to=sid)
