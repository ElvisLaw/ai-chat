## 1. Streaming Consumption

- [x] 1.1 Refactor the streaming chat path to consume synchronous provider generators through a thread-backed producer/consumer boundary
- [x] 1.2 Preserve the existing SSE output contract while propagating stream completion and failure through the new boundary
- [x] 1.3 Ensure the full assistant response is assembled and persisted when streaming completes

## 2. Settings Loading

- [x] 2.1 Update settings resolution to load `.env` from the repository root instead of the process working directory
- [x] 2.2 Replace direct `Settings()` construction in runtime paths with `get_settings()`
- [x] 2.3 Remove or reduce duplicated runtime environment-loading responsibility now superseded by root-based settings resolution

## 3. Verify

- [x] 3.1 Validate that `/chat/stream` still emits the expected SSE sequence without regressing response completion behavior
- [x] 3.2 Validate that runtime configuration still loads when the application is started outside the repository root
- [x] 3.3 Run targeted checks or tests covering stream persistence and shared settings access