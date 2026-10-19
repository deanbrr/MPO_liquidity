"""LF-normalized text hashing (BUILD_SPEC v1.1 §4.1, S-ADR-42): CRLF and LF copies of a file hash equal, binary
files are never normalized, and tree hashes depend on paths and contents only. Owner WP-01."""

from __future__ import annotations

from pathlib import Path

import pytest

from adic_tpa.contracts.errors import SchemaError
from adic_tpa.contracts.hashing import config_hash, engine_tree_hash, file_hash, file_tree_hash, package_root

TEXT = "# model: x:Y\nkey: value\nlist: [1, 2]\n"


def _tree(root: Path, newline: str) -> Path:
    (root / "sub").mkdir(parents=True)
    (root / "a.yaml").write_bytes(TEXT.replace("\n", newline).encode("utf-8"))
    (root / "sub" / "b.py").write_bytes("x = 1\ny = 2\n".replace("\n", newline).encode("utf-8"))
    return root


def test_crlf_and_lf_files_hash_equal(tmp_path: Path) -> None:
    lf, crlf = tmp_path / "lf.yaml", tmp_path / "crlf.yaml"
    lf.write_bytes(TEXT.encode("utf-8"))
    crlf.write_bytes(TEXT.replace("\n", "\r\n").encode("utf-8"))
    assert lf.read_bytes() != crlf.read_bytes()
    assert file_hash(lf) == file_hash(crlf)


def test_crlf_and_lf_trees_hash_equal(tmp_path: Path) -> None:
    assert file_tree_hash(_tree(tmp_path / "lf", "\n")) == file_tree_hash(_tree(tmp_path / "crlf", "\r\n"))


def test_binary_files_are_not_normalized(tmp_path: Path) -> None:
    a, b = tmp_path / "a.npz", tmp_path / "b.npz"
    a.write_bytes(b"\x00\r\n\x01")
    b.write_bytes(b"\x00\n\x01")
    assert file_hash(a) != file_hash(b)


def test_tree_hash_depends_on_paths_and_contents(tmp_path: Path) -> None:
    root = _tree(tmp_path / "t", "\n")
    h0 = file_tree_hash(root)
    (root / "a.yaml").write_text(TEXT + "extra: 1\n", encoding="utf-8")
    h1 = file_tree_hash(root)
    (root / "a.yaml").rename(root / "c.yaml")
    h2 = file_tree_hash(root)
    assert len({h0, h1, h2}) == 3
    (root / "__pycache__").mkdir()
    (root / "__pycache__" / "z.py").write_text("ignored = True\n", encoding="utf-8")
    (root / "notes.txt").write_text("not matched by the default patterns\n", encoding="utf-8")
    assert file_tree_hash(root) == h2


def test_tree_hash_requires_a_directory(tmp_path: Path) -> None:
    with pytest.raises(SchemaError):
        file_tree_hash(tmp_path / "missing")


def test_engine_and_config_hashes() -> None:
    assert package_root().name == "adic_tpa"
    assert engine_tree_hash().startswith("sha256:") and config_hash().startswith("sha256:")
    assert engine_tree_hash() != config_hash()
    assert config_hash() == file_tree_hash(package_root() / "config")
