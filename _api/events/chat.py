from _api.core import sio


@sio.event
async def chat(sid, data):
    text = data.get('text', '').strip()
    if not text:
        return
    await sio.emit('chat_message', {'text': text, 'senderId': sid})
