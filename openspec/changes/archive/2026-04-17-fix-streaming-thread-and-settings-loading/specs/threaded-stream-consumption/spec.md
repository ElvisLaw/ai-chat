## ADDED Requirements

### Requirement: Streaming chat SHALL consume synchronous provider streams off the request path
The chat streaming flow MUST consume synchronous provider stream generators through a worker-thread-backed boundary so that synchronous provider iteration does not block the FastAPI event loop while the SSE response is in progress.

#### Scenario: Streamed response uses thread-backed consumption
- **WHEN** a client calls the streaming chat endpoint
- **THEN** the system MUST consume the provider's synchronous stream generator outside the request-path event loop
- **AND** the endpoint MUST continue emitting SSE chunks in the original response format

#### Scenario: Streaming completion persists assistant response
- **WHEN** the provider stream completes successfully
- **THEN** the system MUST assemble the full assistant response from streamed chunks
- **AND** the completed assistant message MUST be saved to the conversation before the stream is finalized

#### Scenario: Streaming errors surface without hanging the response
- **WHEN** an error occurs while consuming the provider stream
- **THEN** the streaming flow MUST terminate cleanly without leaving the response hanging indefinitely
- **AND** the error MUST be surfaced through the existing API error handling path or stream termination behavior