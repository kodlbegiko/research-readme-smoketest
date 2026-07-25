from __future__ import annotations

import pytest

from readme_smoketest.analyze import classify_block, classify_roles, naive_ready
from readme_smoketest.model import Block, Record


def block(heading: str, text: str, language: str = "bash") -> Block:
    return Block(heading=heading, language=language, text=text)


@pytest.mark.parametrize(
    ("heading", "text"),
    [
        ("Installation", "pip install demo"),
        ("Setup", "npm install"),
        ("Requirements", "conda install demo"),
        ("Quick install", "cmake .."),
        ("Getting Started", "git clone https://example.invalid/demo.git"),
    ],
)
def test_install_roles(heading: str, text: str) -> None:
    assert "install" in classify_roles(block(heading, text))


@pytest.mark.parametrize(
    ("heading", "text", "language"),
    [
        ("Quick start", "print('ok')", "python"),
        ("Usage", "cargo run --example demo", "bash"),
        ("Example", "const x = 1", "javascript"),
        ("Run locally", "npm start", "bash"),
        ("For first-time users", "jupyter lab", "bash"),
    ],
)
def test_first_use_roles(heading: str, text: str, language: str) -> None:
    assert "first_use" in classify_roles(block(heading, text, language))


def test_combined_quick_start_can_install_and_run() -> None:
    roles = classify_roles(
        block(
            "Build Instructions / Quick Start",
            "git clone https://x/y.git\ncmake ..\n./build/app",
        )
    )
    assert {"install", "first_use"} <= roles


def test_test_role() -> None:
    assert "test" in classify_roles(block("Regression tests", "ctest"))


def test_development_role() -> None:
    assert "development" in classify_roles(block("Development", "pip install -e ."))


def test_other_role() -> None:
    assert classify_roles(block("Overview", "This is prose", "text")) == frozenset({"other"})


def test_primary_role_is_deterministic() -> None:
    item = block("Quick Start / Installation", "pip install x\nnpm start")
    assert classify_block(item) == "install"


def make_record(*blocks: Block) -> Record:
    return Record(
        order=1,
        doi="10.test/example",
        title="Example",
        repository="owner/repo",
        host="github",
        readme_sha="abc",
        external_docs=False,
        blocks=tuple(blocks),
        path_index={},
        manual_strict_ready=False,
        manual_hard_defects=(),
        notes="",
    )


def test_naive_ready_accepts_test_as_non_install_block() -> None:
    record = make_record(block("Install", "pip install demo"), block("Tests", "pytest"))
    assert naive_ready(record)


def test_naive_ready_requires_install() -> None:
    record = make_record(block("Quick start", "print('ok')", "python"))
    assert not naive_ready(record)


def test_naive_ready_requires_second_role() -> None:
    record = make_record(block("Install", "pip install demo"))
    assert not naive_ready(record)
