from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

BlockRole = Literal["install", "first_use", "test", "development", "other"]


@dataclass(frozen=True)
class Block:
    heading: str
    language: str
    text: str
    referenced_paths: tuple[str, ...] = ()
    placeholder_explained: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Block:
        return cls(
            heading=str(value.get("heading", "")),
            language=str(value.get("language", "")),
            text=str(value.get("text", "")),
            referenced_paths=tuple(str(x) for x in value.get("referenced_paths", [])),
            placeholder_explained=bool(value.get("placeholder_explained", False)),
        )


@dataclass(frozen=True)
class Record:
    order: int
    doi: str
    title: str
    repository: str
    host: str
    readme_sha: str | None
    external_docs: bool
    blocks: tuple[Block, ...]
    path_index: dict[str, bool]
    manual_strict_ready: bool | None
    manual_hard_defects: tuple[str, ...]
    notes: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Record:
        manual = value.get("manual_strict_ready")
        return cls(
            order=int(value["order"]),
            doi=str(value["doi"]),
            title=str(value["title"]),
            repository=str(value["repository"]),
            host=str(value.get("host", "github")),
            readme_sha=None if value.get("readme_sha") is None else str(value["readme_sha"]),
            external_docs=bool(value.get("external_docs", False)),
            blocks=tuple(Block.from_dict(x) for x in value.get("blocks", [])),
            path_index={str(k): bool(v) for k, v in value.get("path_index", {}).items()},
            manual_strict_ready=None if manual is None else bool(manual),
            manual_hard_defects=tuple(str(x) for x in value.get("manual_hard_defects", [])),
            notes=str(value.get("notes", "")),
        )
