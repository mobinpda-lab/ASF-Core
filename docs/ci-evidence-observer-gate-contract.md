# Gate contract

A promotion matrix row contains `Gate`, `Status`, `Evidence`, `Confidence`, and `Decision`. The decision is `ALLOW` only for `SUCCESS`; all other visibility states are `BLOCK`. This local contract is intentionally stricter than GitHub's empty/pending status semantics and prevents false promotion success.
