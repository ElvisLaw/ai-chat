## ADDED Requirements

### Requirement: Runtime settings SHALL resolve .env from the project root
Application settings MUST resolve `.env` relative to the repository root so runtime configuration remains stable regardless of the process working directory.

#### Scenario: App starts outside repository root
- **WHEN** the application process is launched with a working directory other than the repository root
- **THEN** settings resolution MUST still load values from the project's `.env` file
- **AND** runtime configuration such as API host, API port, CORS origins, and provider credentials MUST remain available

### Requirement: Runtime code SHALL use the shared settings entrypoint
Runtime application code MUST access configuration through `get_settings()` rather than constructing new `Settings()` instances directly.

#### Scenario: Service layer reads default provider model
- **WHEN** the service layer needs runtime configuration such as the default provider model
- **THEN** it MUST obtain configuration through `get_settings()`
- **AND** it MUST not instantiate a separate `Settings()` object for that read

#### Scenario: Server and service use consistent settings state
- **WHEN** server startup code and request-handling code read application settings in the same process
- **THEN** both code paths MUST read configuration through the same shared settings entrypoint
- **AND** the runtime behavior MUST not depend on a mixture of singleton-backed and ad hoc settings instances