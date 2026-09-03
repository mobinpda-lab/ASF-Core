# ASF-Core Security

## Principles
- Least privilege for workers, adapters, and workflows.
- No secrets in source, logs, evidence, schemas, or artifacts.
- Protected branches and required PR gates are mandatory controls.
- Untrusted inputs and adapter states fail closed.
- Security-critical changes require explicit validation and human authorization where policy requires it.

## Supply Chain
Workflow actions and dependencies must be pinned or governed according to repository policy. Validation must detect malformed or unexpected inputs before promotion.

## Evidence
Evidence records integrity-relevant SHA references without exposing credentials or unnecessary sensitive data.

## Incident Handling
Security failures block promotion, enter recovery/incident state, preserve evidence, and resume only after required gates pass.
