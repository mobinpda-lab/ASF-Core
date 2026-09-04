# CI Evidence Provider Resolution

The evidence layer must distinguish authoritative absence from inability to
observe the authoritative source.

| Diagnostic | Required proof | Confidence | Gate behavior |
|---|---|---:|---|
| `AUTHORITATIVE_NOT_FOUND` | Provider explicitly searched the authoritative source and attests no matching execution | HIGH | Evidence may classify as NOT_FOUND; promotion remains subject to gate policy |
| `CI_EXECUTED_NOT_EXPOSED` | Execution is independently known, but its evidence payload is unavailable | LOW | Block |
| `CONNECTOR_OBSERVATION_LIMITATION` | Connector explicitly cannot expose the required provider path | LOW | Block |
| `OBSERVATION_UNCERTAIN` | No authoritative absence or execution proof | LOW | Block |

An empty list alone is never sufficient to prove `NOT_FOUND`. Repository identity
and exact 40-character commit SHA remain mandatory correlation fields. Provider
source, observation state, confidence, reason, and resulting gate decision must
be retained with the observation.
