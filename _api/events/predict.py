from _api.core import sio
from _api.predict import predict_from_buffer


@sio.event
async def predict(sid, data):
    s_buffer = data.get('buffer', '')
    if not s_buffer:
        return
    await sio.emit('predict_return', {'data': predict_from_buffer(s_buffer)},
                   to=sid)
    # await sio.emit('chat_message', {'text': text, 'senderId': sid})
