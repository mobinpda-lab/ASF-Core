# Gate Evidence Store Contract

Evidence storage is append-only and provenance-preserving.

Each publication is immutable and contains the exact commit SHA, normalized gate state, source, observation time, and evidence references. Corrections create a new linked observation rather than mutating history.

The store MUST reject secret material and MUST NOT permit evidence to be detached from its source correlation context.
