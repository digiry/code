# pylint: disable=missing-module-docstring, missing-function-docstring, invalid-name
import shutil
import tempfile
from pathlib import Path

from sync_kkj import sync, determine_actions


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {}

    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))

    assert list(actions) == [("copy", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {"hash1": "fn2"}

    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))

    assert list(actions) == [("move", Path("/dst/fn2"), Path("/dst/fn1"))]
