from typing import Any, Callable

class WorkflowRunCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch=fetch
    def collect(self, repository, commit_sha): return self.fetch(repository=repository, commit_sha=commit_sha)

class CheckRunCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch=fetch
    def collect(self, repository, commit_sha): return self.fetch(repository=repository, commit_sha=commit_sha)

class JobResultCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch=fetch
    def collect(self, repository, run_id): return self.fetch(repository=repository, run_id=run_id)

class ArtifactResultCollector:
    def __init__(self, fetch: Callable[..., Any]): self.fetch=fetch
    def collect(self, repository, run_id): return self.fetch(repository=repository, run_id=run_id)
