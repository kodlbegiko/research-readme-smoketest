from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "acquire_issue_121.py"


def load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("acquire_issue_121", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extract_blocks_tracks_heading_language_paths_and_placeholder() -> None:
    module = load_script()
    text = """# Quick start
Replace `<input>` with your local file.

```python
import demo
result = demo.run('examples/input.csv')
```
"""
    blocks = module.extract_blocks(text)
    assert blocks == [
        {
            "heading": "Quick start",
            "language": "python",
            "text": "import demo\nresult = demo.run('examples/input.csv')",
            "referenced_paths": ["examples/input.csv"],
        }
    ]


def test_external_documentation_accepts_explicit_docs_not_badges() -> None:
    module = load_script()
    positive = "See the [user guide](https://example.org/docs/guide.html)."
    negative = "[build](https://img.shields.io/badge/build-passing-green)"
    assert module.external_documentation(positive)[0] is True
    assert module.external_documentation(negative)[0] is False


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("examples/data.csv", "examples/data.csv"),
        ("https://example.org/data.csv", None),
        ("../secret/data.csv", None),
        ("output", None),
        ("<path>/data.csv", None),
    ],
)
def test_clean_path_boundaries(raw: str, expected: str | None) -> None:
    module = load_script()
    assert module.clean_path(raw) == expected


def test_sampling_frame_is_complete_and_ordered() -> None:
    module = load_script()
    frame = module.read_json(Path("data/issue-121/sampling-frame.json"))
    assert len(frame) == 39
    assert [item["order"] for item in frame] == list(range(1, 40))
    assert sum(item["host"] == "gitlab" for item in frame) == 1
