from __future__ import annotations

import pytest

from readme_smoketest.analyze import block_defects, substitution_required
from readme_smoketest.model import Block


def test_missing_git_clone_target() -> None:
    item = Block("Setup", "bash", "git clone --recurse-submodules")
    assert block_defects(item, {}) == ["missing_git_clone_target"]


def test_git_clone_target_present() -> None:
    item = Block("Setup", "bash", "git clone --depth 1 https://github.com/a/b.git")
    assert block_defects(item, {}) == []


def test_apt_get_typo() -> None:
    item = Block("Requirements", "bash", "sudo apt get update")
    assert block_defects(item, {}) == ["apt_get_typo"]


def test_apt_get_hyphen_is_not_typo() -> None:
    item = Block("Requirements", "bash", "sudo apt-get update")
    assert block_defects(item, {}) == []


def test_missing_relative_path() -> None:
    item = Block("Example", "python", "open('missing.csv')", ("missing.csv",))
    assert block_defects(item, {"missing.csv": False}) == ["missing_relative_path:missing.csv"]


def test_existing_relative_path() -> None:
    item = Block("Example", "python", "open('data.csv')", ("data.csv",))
    assert block_defects(item, {"data.csv": True}) == []


def test_unknown_path_is_not_claimed_missing() -> None:
    item = Block("Example", "python", "open('unknown.csv')", ("unknown.csv",))
    assert block_defects(item, {}) == []


def test_undeclared_module_assignment() -> None:
    text = "import * as Demo from 'demo';\nviewer = new Demo.Viewer();"
    item = Block("Usage", "javascript", text)
    assert block_defects(item, {}) == ["undeclared_module_assignment:viewer"]


def test_declared_module_assignment() -> None:
    text = "import * as Demo from 'demo';\nconst viewer = new Demo.Viewer();"
    item = Block("Usage", "javascript", text)
    assert block_defects(item, {}) == []


def test_classic_script_bare_assignment_is_not_flagged() -> None:
    item = Block("Usage", "javascript", "viewer = new Demo.Viewer();")
    assert block_defects(item, {}) == []


def test_duplicate_defects_are_deduplicated() -> None:
    item = Block("Requirements", "bash", "sudo apt get update\nsudo apt get update")
    assert block_defects(item, {}) == ["apt_get_typo"]


@pytest.mark.parametrize("text", ["pip install <package>", "./app <input>", "cd <path>"])
def test_unexplained_placeholder_requires_substitution(text: str) -> None:
    assert substitution_required(Block("Usage", "bash", text))


def test_explained_placeholder_is_allowed() -> None:
    assert not substitution_required(
        Block("Usage", "bash", "./app <input>", placeholder_explained=True)
    )


def test_plain_command_needs_no_substitution() -> None:
    assert not substitution_required(Block("Usage", "bash", "./app data.csv"))
