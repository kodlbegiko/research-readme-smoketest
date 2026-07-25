from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from .model import Block, BlockRole, Record

INSTALL_TERMS = (
    "install",
    "setup",
    "requirements",
    "getting started",
    "quick install",
    "build instructions",
)
FIRST_USE_TERMS = ("quick start", "quickstart", "usage", "example", "run", "first-time")
TEST_TERMS = ("test", "testing", "verification", "regression")
DEV_TERMS = ("development", "developer", "contributing", "monorepo")
INSTALL_COMMANDS = (
    "pip install",
    "python -m pip install",
    "conda install",
    "conda env create",
    "npm install",
    "cargo add",
    "cmake ",
    "cmake\n",
    "julia",
    "pkg> instantiate",
    "add tikhonovfenichelreductions",
    "git clone",
)
FIRST_USE_COMMANDS = (
    "cargo run",
    "npm start",
    "jupyter lab",
    "jupyter notebook",
    "nextflow run",
    "streamlit run",
    "java -jar",
    "./build/",
)
ANGLE_PLACEHOLDER = re.compile(r"<[^>\n]+>")
BARE_JS_ASSIGNMENT = re.compile(r"(?m)^\s*([A-Za-z_$][\w$]*)\s*=\s*new\s+")
DECLARED_JS = re.compile(r"(?m)^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=")


def _norm(value: str) -> str:
    return " ".join(value.lower().replace("_", " ").replace("-", " ").split())


def classify_roles(block: Block) -> frozenset[BlockRole]:
    """Return every role a block can safely serve.

    A single quick-start shell block can both install and invoke a program. Treating
    roles as mutually exclusive would miss that common documentation pattern.
    """

    heading = _norm(block.heading)
    text = block.text.lower()
    roles: set[BlockRole] = set()

    if any(term in heading for term in TEST_TERMS):
        roles.add("test")
    if any(term in heading for term in DEV_TERMS):
        roles.add("development")
    if any(cmd in text for cmd in INSTALL_COMMANDS):
        if any(term in heading for term in INSTALL_TERMS) or "git clone" in text:
            roles.add("install")
    if any(term in heading for term in FIRST_USE_TERMS):
        if any(cmd in text for cmd in FIRST_USE_COMMANDS):
            roles.add("first_use")
        elif block.language.lower() in {
            "python",
            "py",
            "javascript",
            "js",
            "typescript",
            "ts",
            "rust",
        }:
            roles.add("first_use")
    if any(cmd in text for cmd in FIRST_USE_COMMANDS):
        roles.add("first_use")
    if any(cmd in text for cmd in INSTALL_COMMANDS) and not roles:
        roles.add("install")
    if not roles:
        roles.add("other")
    return frozenset(roles)


def classify_block(block: Block) -> BlockRole:
    """Return a deterministic primary role for compact tabular output."""

    roles = classify_roles(block)
    priority: tuple[BlockRole, ...] = ("install", "first_use", "test", "development", "other")
    for role in priority:
        if role in roles:
            return role
    return "other"


def block_defects(block: Block, path_index: dict[str, bool]) -> list[str]:
    defects: list[str] = []
    lowered = block.text.lower()
    for raw_line in block.text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("git clone"):
            tokens = line.split()
            non_options = [token for token in tokens[2:] if not token.startswith("-")]
            if not non_options:
                defects.append("missing_git_clone_target")
        if re.search(r"\bsudo\s+apt\s+get\b", line):
            defects.append("apt_get_typo")
    for path in block.referenced_paths:
        if path_index.get(path) is False:
            defects.append(f"missing_relative_path:{path}")
    if block.language.lower() in {"js", "javascript", "ts", "typescript"} and "import " in lowered:
        declared = set(DECLARED_JS.findall(block.text))
        for name in BARE_JS_ASSIGNMENT.findall(block.text):
            if name not in declared:
                defects.append(f"undeclared_module_assignment:{name}")
    return sorted(set(defects))


def substitution_required(block: Block) -> bool:
    return bool(ANGLE_PLACEHOLDER.search(block.text)) and not block.placeholder_explained


def naive_ready(record: Record) -> bool:
    roles = [classify_roles(block) for block in record.blocks]
    has_install = any("install" in block_roles for block_roles in roles)
    has_any_runnable_non_install = any(
        bool(block_roles & {"first_use", "test", "development"}) for block_roles in roles
    )
    return has_install and has_any_runnable_non_install


def analyze_record(record: Record) -> dict[str, Any]:
    if record.host != "github":
        return {
            "order": record.order,
            "repository": record.repository,
            "eligible": False,
            "exclusion_reason": "non_github",
        }

    analyzed_blocks: list[dict[str, Any]] = []
    install_safe = False
    first_use_safe = False
    all_defects: list[str] = []
    substitution_blocks = 0

    for block in record.blocks:
        roles = classify_roles(block)
        defects = block_defects(block, record.path_index)
        needs_substitution = substitution_required(block)
        if needs_substitution:
            substitution_blocks += 1
        if "install" in roles and not defects and not needs_substitution:
            install_safe = True
        if "first_use" in roles and not defects and not needs_substitution:
            first_use_safe = True
        all_defects.extend(defects)
        analyzed_blocks.append(
            {
                "heading": block.heading,
                "language": block.language,
                "roles": sorted(roles),
                "defects": defects,
                "substitution_required": needs_substitution,
            }
        )

    strict_ready = install_safe and first_use_safe
    return {
        "order": record.order,
        "doi": record.doi,
        "title": record.title,
        "repository": record.repository,
        "eligible": True,
        "readme_sha": record.readme_sha,
        "external_docs": record.external_docs,
        "install_safe": install_safe,
        "first_use_safe": first_use_safe,
        "strict_ready": strict_ready,
        "relaxed_ready": strict_ready or record.external_docs,
        "naive_ready": naive_ready(record),
        "hard_defects": sorted(set(all_defects)),
        "substitution_blocks": substitution_blocks,
        "manual_strict_ready": record.manual_strict_ready,
        "manual_hard_defects": list(record.manual_hard_defects),
        "blocks": analyzed_blocks,
        "notes": record.notes,
    }


def analyze_records(records: Iterable[Record]) -> list[dict[str, Any]]:
    return [analyze_record(record) for record in records]
