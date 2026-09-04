"""Generic project adapter boundary.

Adapters translate project-specific execution surfaces into factory contracts.
No product implementation belongs in ASF-Core.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from factory.contracts.schema import ProjectContract, Task


class ProjectAdapter(Protocol):
    def validate_contract(self, project: ProjectContract) -> None: ...
    def branch_name(self, task: Task) -> str: ...
    def execution_command(self, task: Task) -> list[str]: ...


@dataclass(frozen=True)
class GenericAdapter:
    name: str = "generic"

    def validate_contract(self, project: ProjectContract) -> None:
        if not project.project_id or not project.repository:
            raise ValueError("project_id and repository are required")
        if not project.default_branch:
            raise ValueError("default_branch is required")
        if not project.ci_contract:
            raise ValueError("ci_contract is required")
        if not project.completion_definition:
            raise ValueError("completion_definition is required")

    def branch_name(self, task: Task) -> str:
        safe = task.task_id.replace("/", "-").replace(" ", "-")
        return f"factory/task/{task.project_id}/{safe}"

    def execution_command(self, task: Task) -> list[str]:
        return ["factory-worker", "execute", "--task", task.task_id]
