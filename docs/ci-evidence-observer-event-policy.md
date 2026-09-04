# Event correlation policy

Workflow event type is retained as authoritative metadata and must be evaluated by downstream gate policy. A run on the wrong event or stale head cannot be used as exact-head promotion evidence. The observer rejects identity mismatches rather than guessing intent.
