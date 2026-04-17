## Why

The recent high-priority fixes improved the chat and settings paths, but two root issues remain unresolved. The streaming endpoint still consumes the synchronous LLM generator on the request path, and settings loading still depends on the current working directory while some code paths bypass the shared settings accessor.

## What Changes

- Move streaming chunk consumption off the request path so synchronous LLM stream iteration happens in a worker-thread-backed flow rather than on the event loop.
- Restore project-root-based `.env` resolution so application settings load consistently regardless of the process working directory.
- Standardize settings access on `get_settings()` instead of mixing singleton access with direct `Settings()` construction.

## Capabilities

### New Capabilities
- `threaded-stream-consumption`: Ensure streaming chat responses consume synchronous provider generators without blocking the FastAPI event loop.
- `root-settings-loading`: Ensure application settings resolve `.env` from the project root and are accessed through the shared settings entrypoint.

### Modified Capabilities

## Impact

- `src/ai_chat/api/routes/chat.py`: adjust streaming response flow so synchronous stream iteration does not run on the request path.
- `src/ai_chat/conversation/service.py`: align stream orchestration and settings access with the shared runtime behavior.
- `src/ai_chat/settings.py`: restore stable project-root `.env` discovery and centralize singleton-based settings access.
- `src/ai_chat/config.py`: likely reduce or absorb duplicated environment loading responsibility.