from __future__ import annotations

from readme_smoketest.analyze import analyze_record, analyze_records
from readme_smoketest.model import Block, Record


def record(
    *blocks: Block,
    host: str = "github",
    external_docs: bool = False,
    path_index: dict[str, bool] | None = None,
) -> Record:
    return Record(
        order=1,
        doi="10.test/example",
        title="Example",
        repository="owner/repo",
        host=host,
        readme_sha="abc",
        external_docs=external_docs,
        blocks=tuple(blocks),
        path_index=path_index or {},
        manual_strict_ready=False,
        manual_hard_defects=(),
        notes="note",
    )


def test_non_github_record_is_excluded() -> None:
    result = analyze_record(record(host="gitlab"))
    assert not result["eligible"]
    assert result["exclusion_reason"] == "non_github"


def test_safe_install_and_first_use_is_strict_ready() -> None:
    result = analyze_record(
        record(
            Block("Installation", "bash", "pip install demo"),
            Block("Quick start", "python", "print('ok')"),
        )
    )
    assert result["strict_ready"]


def test_missing_first_use_is_not_strict_ready() -> None:
    result = analyze_record(record(Block("Installation", "bash", "pip install demo")))
    assert not result["strict_ready"]


def test_external_docs_only_affect_relaxed_definition() -> None:
    result = analyze_record(
        record(Block("Installation", "bash", "pip install demo"), external_docs=True)
    )
    assert not result["strict_ready"]
    assert result["relaxed_ready"]


def test_defective_first_use_does_not_count_as_safe() -> None:
    item = Block("Usage", "javascript", "import X from 'x';\napp = new X();")
    result = analyze_record(record(Block("Install", "bash", "npm install x"), item))
    assert not result["first_use_safe"]
    assert result["hard_defects"] == ["undeclared_module_assignment:app"]


def test_one_bad_example_does_not_cancel_separate_good_example() -> None:
    bad = Block("Example", "python", "open('bad.csv')", ("bad.csv",))
    good = Block("Example", "python", "print('ok')")
    result = analyze_record(
        record(Block("Install", "bash", "pip install x"), bad, good, path_index={"bad.csv": False})
    )
    assert result["strict_ready"]
    assert result["hard_defects"] == ["missing_relative_path:bad.csv"]


def test_substitution_block_count() -> None:
    result = analyze_record(record(Block("Install", "bash", "pip install <package>")))
    assert result["substitution_blocks"] == 1


def test_analyze_records_preserves_order() -> None:
    first = record(Block("Install", "bash", "pip install a"))
    second = Record(**{**first.__dict__, "order": 2, "repository": "owner/second"})
    results = analyze_records([first, second])
    assert [row["order"] for row in results] == [1, 2]
