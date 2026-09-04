# Implementation note

The current observer is deliberately adapter-oriented: it normalizes authoritative source observations rather than pretending the connector itself is a CI backend. This separation permits GitHub REST, Checks, Actions and future providers to feed the same fail-closed gate contract.

The observer does not infer artifact existence, does not turn empty statuses into success, and rejects stale or cross-repository observations. Production promotion must consume authoritative evidence exposed by the adapter and remain under Production Orchestrator control.
