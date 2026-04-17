## 1. Modify chat() method

- [x] 1.1 Import `asyncio` in `service.py`
- [x] 1.2 Wrap `client.send_message()` call with `asyncio.to_thread()` in `chat()` method

## 2. Modify stream() method

- [x] 2.1 Handle synchronous `stream_message()` — `stream()` stays sync def, called via `to_thread` in `chat_stream` route
- [x] 2.2 Ensure conversation save still happens after streaming completes

## 3. Verify

- [x] 3.1 Run API health check: `curl http://localhost:8000/health` ✓
- [x] 3.2 Test synchronous chat endpoint: `curl -X POST http://localhost:8000/chat -d '{"message":"hello"}'` ✓
- [x] 3.3 Test streaming chat endpoint: `curl -X POST http://localhost:8000/chat/stream -d '{"message":"hello"}'` ✓
