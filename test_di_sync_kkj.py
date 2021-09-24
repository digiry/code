from pathlib import Path

from sync_kkj import synchronize_dirs


class FakeFileSystem(list):
    def copy(self, src, dest):
        self.append(("copy", src, dest))

    def move(self, src, dest):
        self.append(("move", src, dest))

    def delete(self, dest):
        self.append(("delete", dest))


def test_whan_a_file_exists_in_the_source_but_not_the_destination():
    source = {"sha1": "my-file"}
    dest = {}
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronize_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [("copy", Path("/source/my-file"), Path("/dest/my-file"))]


def test_when_a_file_has_been_renamed_in_the_source():
    source = {"sha1": "renamed-file"}
    dest = {"sha1": "original-file"}
    filesystem = FakeFileSystem()

    reader = {"/source": source, "/dest": dest}
    synchronize_dirs(reader.pop, filesystem, "/source", "/dest")

    assert filesystem == [
        ("move", Path("/dest/original-file"), Path("/dest/renamed-file"))
    ]
