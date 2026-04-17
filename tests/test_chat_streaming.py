import threading

from fastapi.testclient import TestClient

from app.api.dependencies import get_chat_service
from app.api.server import create_app


class FakeStreamingService:
    def __init__(self) -> None:
        self.stream_called_thread: int | None = None
        self.iterated_thread: int | None = None

    def stream(self, **kwargs):
        self.stream_called_thread = threading.get_ident()

        def generate():
            self.iterated_thread = threading.get_ident()
            yield "hello"
            yield "world"

        return generate(), "conv-123"


def test_chat_stream_consumes_generator_off_request_path() -> None:
    app = create_app()
    service = FakeStreamingService()
    app.dependency_overrides[get_chat_service] = lambda: service

    with TestClient(app) as client:
        with client.stream("POST", "/chat/stream", json={"message": "hi"}) as response:
            payload = []
            for raw_line in response.iter_lines():
                line = raw_line.decode() if isinstance(raw_line, bytes) else raw_line
                if line.startswith("data: "):
                    payload.append(line.removeprefix("data: ").strip())

    assert payload == ["conv-123", "hello", "world", "[DONE]"]
    assert service.stream_called_thread is not None
    assert service.iterated_thread is not None
    assert service.iterated_thread != service.stream_called_thread