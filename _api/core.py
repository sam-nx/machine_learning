import socketio
import logging

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*',
                           logger=False, engineio_logger=False,
                           max_http_buffer_size=10_000_000)


class SuppressSocketIOLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return ("/socket.io/" not in message
                and "WebSocket /socket.io/" not in message)


uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.addFilter(SuppressSocketIOLogs())

app = socketio.ASGIApp(sio)
