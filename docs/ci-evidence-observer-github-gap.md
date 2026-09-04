# GitHub evidence visibility gap

If the GitHub integration returns no workflow/check/status objects, the observer cannot distinguish a genuinely absent CI execution from evidence that is not exposed by the integration surface. The adapter must preserve that distinction using `NOT_FOUND` only for authoritative absence and `NOT_EXPOSED` when access/visibility is unavailable.
