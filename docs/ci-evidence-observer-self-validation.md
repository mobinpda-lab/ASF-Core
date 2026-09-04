# Self-validation protocol

For ASF-Core self-observation, the requested repository and exact commit SHA are mandatory inputs. The observer must collect workflow runs, check runs, jobs, artifacts, and commit statuses from authoritative sources. Every item is correlated to repository identity and SHA before classification.

A source that is inaccessible is `NOT_EXPOSED`; an authoritative empty result is `NOT_FOUND`. Neither state is success. The gate integration is fail-closed and therefore blocks promotion for all non-success states.

PR #2 must be observed at its exact head `6a26f23572a951642b4dea3b17d6a8f672b56e1f`. PR #3 must be observed at its current exact head. Absence of exposed CI runs/statuses must remain visible as an evidence gap rather than being converted into a synthetic success.
