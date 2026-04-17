## Context

The current chat flow already moved non-streaming provider calls behind `asyncio.to_thread`, but the streaming path still returns a synchronous generator that is iterated on the request path. That means the blocking provider stream is still consumed from the FastAPI request lifecycle, so the event loop can still be tied up during long responses.

Settings access also became inconsistent after introducing `get_settings()`. Some code paths still instantiate `Settings()` directly, and the `env_file=".env"` configuration depends on the process working directory rather than the repository root. The older `config.py` logic had more stable root-relative discovery, but the current runtime no longer consistently uses it.

## Goals / Non-Goals

**Goals:**
- Ensure synchronous provider streaming is consumed outside the event-loop request path.
- Restore deterministic `.env` discovery from the project root.
- Make `get_settings()` the single runtime entrypoint for settings reads.
- Keep the public API and request/response contracts unchanged.

**Non-Goals:**
- Do not replace the provider SDKs with native async clients.
- Do not redesign the SSE payload format.
- Do not introduce new configuration files or environment variable names.

## Decisions

### Decision 1: Bridge synchronous stream consumption through a thread-backed producer/consumer boundary

The route should no longer iterate the provider generator directly. Instead, the synchronous stream should be consumed inside a worker thread, and chunks should be handed back to the HTTP response path through a thread-safe boundary.

Preferred implementation shape:
- Keep provider clients synchronous.
- Start a worker-thread function that iterates `client.stream_message(...)` to completion.
- Push chunks and terminal state through a queue-like handoff.
- Expose an async-friendly response iterator that reads from that handoff and emits SSE frames.

Why this approach:
- It fixes the actual blocking point instead of only moving generator creation.
- It preserves existing provider client code and avoids a larger SDK rewrite.
- It keeps conversation save semantics tied to stream completion.

Alternatives considered:
- Only wrap `service.stream(...)` in `asyncio.to_thread`: rejected because generator iteration remains lazy and still happens on the request path.
- Convert routes back to synchronous handlers: rejected because it gives up the async integration surface without solving future async composition needs.
- Replace OpenAI/Anthropic clients with async SDK variants: rejected as too large for this change.

### Decision 2: Resolve `.env` from the repository root in settings.py

The settings module should own root-relative `.env` discovery rather than depending on the caller's current working directory. The simplest stable approach is to compute the project root from `settings.py` and pass the resulting absolute path into `SettingsConfigDict`.

Why this approach:
- It restores the predictable behavior that existed before the singleton refactor.
- It keeps configuration logic in one place instead of splitting responsibility between `settings.py` and `config.py`.
- It avoids requiring callers to launch the app from a specific directory.

Alternatives considered:
- Keep `env_file=".env"`: rejected because it is cwd-sensitive.
- Reintroduce explicit `load_config()` calls in application startup: rejected because it recreates timing and duplication problems.
- Keep both dotenv loading paths active: rejected because dual sources of truth make behavior harder to reason about.

### Decision 3: Replace direct `Settings()` construction with `get_settings()` in runtime paths

Service and API code should use `get_settings()` exclusively. That keeps configuration access consistent, reduces repeated instantiation, and makes later caching or test overrides more straightforward.

Why this approach:
- It matches the current architecture already used by server startup.
- It prevents subtle divergence between singleton-backed and directly-instantiated settings objects.
- It narrows the runtime configuration contract to one entrypoint.

## Risks / Trade-offs

- [Risk] Queue/thread coordination can introduce stream-finalization bugs or dropped terminal events. -> Mitigation: use an explicit sentinel for completion and ensure exception paths also publish terminal state.
- [Risk] Conversation persistence could be skipped if the worker thread exits early. -> Mitigation: keep assistant-message save logic in the same worker-controlled completion flow and cover it with a regression test.
- [Trade-off] Thread-backed streaming adds a small amount of complexity compared with direct iteration. -> Mitigation: keep the boundary narrow and local to chat streaming orchestration.
- [Trade-off] Centralizing `.env` resolution in `settings.py` reduces the role of `config.py`. -> Mitigation: either demote `config.py` to compatibility glue or remove duplicated behavior in a follow-up cleanup.