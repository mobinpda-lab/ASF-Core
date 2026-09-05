"""Small GitHub REST client used by NIRA runtime components.

The client is deliberately dependency-free so it can run inside GitHub Actions.
It reads the token from the environment and never invents remote state.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class GitHubAPIError(RuntimeError):
    """Raised when GitHub rejects or cannot answer a NIRA observation."""


class GitHubClient:
    def __init__(self, token: str | None = None, api_base: str = "https://api.github.com") -> None:
        self.token = (token or os.getenv("GITHUB_TOKEN", "")).strip()
        if not self.token:
            raise ValueError("GITHUB_TOKEN is required")
        self.api_base = api_base.rstrip("/")

    def get(self, path: str) -> Any:
        if not path.startswith("/"):
            raise ValueError("GitHub API path must start with '/'")
        request = urllib.request.Request(
            f"{self.api_base}{path}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[-4000:]
            raise GitHubAPIError(f"GitHub GET {path} failed: HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise GitHubAPIError(f"GitHub GET {path} failed: {exc}") from exc

    def repository(self, repo: str) -> dict[str, Any]:
        return self.get(f"/repos/{repo}")

    def pull_request(self, repo: str, number: int) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/pulls/{number}")

    def commit_status(self, repo: str, sha: str) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/commits/{sha}/status")

    def check_runs(self, repo: str, sha: str) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/commits/{sha}/check-runs?per_page=100")

    def workflow_runs_for_head(self, repo: str, sha: str) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/actions/runs?head_sha={sha}&per_page=100")

    def workflow_run(self, repo: str, run_id: int) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/actions/runs/{run_id}")

    def workflow_run_jobs(self, repo: str, run_id: int) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/actions/runs/{run_id}/jobs?per_page=100")

    def workflow_run_artifacts(self, repo: str, run_id: int) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100")

    def compare(self, repo: str, base_sha: str, head_sha: str) -> dict[str, Any]:
        return self.get(f"/repos/{repo}/compare/{base_sha}...{head_sha}")
