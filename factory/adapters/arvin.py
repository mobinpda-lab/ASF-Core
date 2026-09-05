"""NIRA-owned Arvin client adapter.

This module is deliberately declarative: it exposes only product execution
metadata and constraints. Queue, lease, worker, gate, evidence, and promotion
authority remain in the NIRA control plane.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArvinClientAdapter:
    project_id: str = "arvin-clean"
    repository: str = "mobinpda-lab/Arvin-clean"
    default_branch: str = "main"
    provider: str = "github"
    build_commands: tuple[tuple[str, ...], ...] = (("flutter", "build", "apk", "--debug"),)
    test_commands: tuple[tuple[str, ...], ...] = (("flutter", "test"), ("flutter", "analyze"))
    security_constraints: tuple[str, ...] = (
        "no-direct-main-mutation",
        "exact-base-required",
        "exact-head-required",
        "required-ci-success",
    )
    deployment_constraints: tuple[str, ...] = (
        "promotion-controlled-by-nira",
        "release-controlled-by-nira",
    )

    @property
    def allowed_fields(self) -> frozenset[str]:
        return frozenset({
            "project_id",
            "repository",
            "default_branch",
            "provider",
            "build_commands",
            "test_commands",
            "security_constraints",
            "deployment_constraints",
        })

    def validate(self) -> None:
        if not self.project_id or not self.repository:
            raise ValueError("Arvin adapter identity is required")
        if self.default_branch != "main":
            raise ValueError("Arvin must target main as its protected base")
        if not self.build_commands or not self.test_commands:
            raise ValueError("Arvin build/test commands are required")
        required = {
            "no-direct-main-mutation",
            "exact-base-required",
            "exact-head-required",
            "required-ci-success",
        }
        if not required.issubset(self.security_constraints):
            raise ValueError("Arvin security constraints are incomplete")
        if "promotion-controlled-by-nira" not in self.deployment_constraints:
            raise ValueError("promotion authority must remain in NIRA")
