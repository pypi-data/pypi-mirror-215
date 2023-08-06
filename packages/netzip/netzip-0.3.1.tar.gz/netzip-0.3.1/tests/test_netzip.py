import io
import zipfile
import zlib

import pytest

from netzip import Archive, FileSource

CONTENTS = {
    "small": (
        {
            b"spam.txt": (b"SPAM!", b"spammy comment"),
            b"eggs/ham.bin": (b"\xDE\xAD\xBE\xEF", b"beefy comment"),
            b"empty": (b"", b""),
        },
        b"small comment",
    ),
    "zip64": (
        {f"spam-{i:04X}.txt".encode(): (b"SPAM!", b"^_^") for i in range(0x10000)},
        b"large comment",
    ),
}


@pytest.fixture(scope="class")
def archive(name) -> Archive:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w") as zf:
        zf.comment = CONTENTS[name][1]
        for name, (data, comment) in CONTENTS[name][0].items():
            zi = zipfile.ZipInfo(name.decode())
            zi.comment = comment
            zf.writestr(zi, data)
    return Archive(FileSource(buf))


@pytest.mark.parametrize("name", CONTENTS, scope="class")
class TestArchive:
    def test_getitem(self, name, archive):
        for name, (data, _comment) in CONTENTS[name][0].items():
            assert archive[name] == data

    def test_iter(self, name, archive):
        assert set(archive) == set(CONTENTS[name][0])

    def test_len(self, name, archive):
        assert len(archive) == len(CONTENTS[name][0])

    def test_comment(self, name, archive):
        assert archive.comment == CONTENTS[name][1]

    def test_file_names(self, name, archive):
        assert set(archive.files) == set(CONTENTS[name][0])

    def test_file_keys_match_names(self, archive):
        for name, file in archive.files.items():
            assert name == file.name

    def test_file_comments(self, name, archive):
        for file in archive.files.values():
            assert file.comment == CONTENTS[name][0][file.name][1]

    def test_crc32(self, name, archive):
        for file in archive.files.values():
            crc32 = zlib.crc32(CONTENTS[name][0][file.name][0])
            assert file.crc32 == crc32
            assert zlib.crc32(archive[file.name]) == crc32
