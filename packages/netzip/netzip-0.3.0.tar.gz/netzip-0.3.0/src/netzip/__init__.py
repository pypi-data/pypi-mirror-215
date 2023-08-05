import abc
import io
import zlib
from dataclasses import dataclass
from typing import Iterable, Mapping

_MULTIDISK_ERRMSG = "Multi-disk archives are not supported"
_ENCRYPTED_ERRMSG = "Encrypted archives are not supported"
_COMPRESSED_ERRMSG = "Compressed archives are not supported"


class _Buffer:
    """Simple buffer for reading bytes and numbers from a byte string."""

    def __init__(self, data: bytes):
        """Create a new buffer that reads values from the given byte string."""
        self._data = data
        self._offset = 0

    def read(self, size: int = -1) -> bytes:
        """Read the given number of bytes.

        If size is negative, read all remaining bytes.
        Raise ValueError if offset or offse + size are out of bounds.
        """
        start = self._offset
        stop = start + size if size >= 0 else len(self._data)
        if stop > len(self._data):
            raise ValueError(f"Buffer underflow: {stop} > {len(self._data)}")
        self._offset = stop
        return self._data[start:stop]

    def move(self, delta: int) -> int:
        """Move the current offset by the given (potentially negative) delta.

        Return the new offset.
        Raise ValueError if the new offset is out of bounds.
        """
        n = self._offset + delta
        if not (0 <= n < len(self._data)):
            raise ValueError(f"Offset is out of bounds: {n}")
        self._offset = n
        return n

    def end(self) -> bool:
        """Return True if the buffer is at the end."""
        return self._offset >= len(self._data)

    def match(self, expected: bytes) -> None:
        """Raise ValueError if the next bytes are not equal to the given bytes."""
        found = self.read(len(expected))
        if found != expected:
            raise ValueError(f"Found {found}, but expected {expected}")

    def number(self, size: int) -> int:
        """Read a little-endian, unsigned integer of the given size in bytes."""
        return int.from_bytes(self.read(size), byteorder="little")

    def number_match(self, size: int, expected: int, msg: str) -> None:
        """Raise ValueError if the next bytes are not equal to the given number."""
        if self.number(size) != expected:
            raise ValueError(msg)


class Source(abc.ABC):
    """Abstract base class for reading bytes from a source."""

    @abc.abstractmethod
    def read(self, offset: int, size: int = -1) -> bytes:
        """Read the given number of bytes at the specified offset.

        If offset is negative, it is relative to the end of the source.
        If size is negative, read all remaining bytes.
        """
        pass

    @abc.abstractmethod
    def size(self) -> int:
        """Return the total number of bytes in the source.

        Implementations are highliy recommended to cache the result.
        """
        pass


class FileSource(Source):
    """Read bytes from a file-like object."""

    def __init__(self, fd: io.BufferedIOBase) -> None:
        """Create a new source that reads bytes from the given file-like object.

        The file handle should be opened in binary mode, and should not be closed
        while the source is in use.
        """
        self._fd = fd
        self._size = -1

    def read(self, offset: int, size: int = -1) -> bytes:
        # Convert relative negative offset to positive absolute offset
        # because fseek() from the C standard library sets errno to EINVAL
        # if the effective absolute position is negative.
        if offset < 0:
            offset = max(0, self.size() + offset)
        self._fd.seek(offset)
        return self._fd.read(size)

    def size(self) -> int:
        if self._size < 0:
            self._size = self._fd.seek(0, io.SEEK_END)
        return self._size


@dataclass
class File:
    """Information about a file in an archive."""

    name: bytes
    offset: int
    size: int
    crc32: int
    comment: bytes


class Archive:
    """ZIP archive reader.

    Supports ZIP64, but does not support compressed, multi-disk, and encrypted archives.
    """

    source: Source
    comment: bytes
    files: Mapping[bytes, File]

    def __init__(self, source: Source) -> None:
        """Create a new archive, and read all the necessary metadata from the source."""
        self.source = source

        # Read data block large enough to contain EOCD record with maximum-sized
        # comment field, and ZIP64 EOCD locator.
        eocd_block = source.read(-65577)

        # Find the start of EOCD record.
        eocd_offset = eocd_block.rfind(b"\x50\x4b\x05\x06")
        if eocd_offset < 0:
            raise ValueError("Could not find end of central directory")

        # Parse EOCD record.
        eocd = _Buffer(eocd_block[eocd_offset:])
        eocd.move(4)
        eocd.number_match(2, 0, _MULTIDISK_ERRMSG)
        eocd.number_match(2, 0, _MULTIDISK_ERRMSG)
        entries = eocd.number(2)
        eocd.number_match(2, entries, _MULTIDISK_ERRMSG)
        cdsize = eocd.number(4)
        cdoffset = eocd.number(4)
        self.comment = eocd.read(eocd.number(2))
        if not eocd.end():
            raise ValueError("Unexpected data after end of central directory")

        # If this is a ZIP64 archive, the actual offset and size of the central
        # directory are stored elsewhere.
        if entries == 0xFFFF or cdsize == 0xFFFFFFFF or cdoffset == 0xFFFFFFFF:
            # Parse ZIP64 EOCD locator.
            if eocd_offset < 20:
                raise ValueError("ZIP64 end of central directory locator not found")
            loc = _Buffer(eocd_block[eocd_offset - 20 : eocd_offset])
            loc.match(b"\x50\x4b\x06\x07")
            loc.number_match(4, 0, _MULTIDISK_ERRMSG)
            eocd64_offset = loc.number(8)
            loc.number_match(4, 1, _MULTIDISK_ERRMSG)

            # Parse ZIP64 EOCD record.
            eocd64 = _Buffer(source.read(eocd64_offset, 56))
            eocd64.match(b"\x50\x4b\x06\x06")
            eocd64.number_match(8, 44, "ZIP64 extensible data is not supported")
            eocd64.move(4)
            eocd64.number_match(4, 0, _MULTIDISK_ERRMSG)
            eocd64.number_match(4, 0, _MULTIDISK_ERRMSG)
            entries = eocd64.number(8)
            eocd64.number_match(8, entries, _MULTIDISK_ERRMSG)
            cdsize = eocd64.number(8)
            cdoffset = eocd64.number(8)

        if cdoffset + cdsize > source.size():
            raise ValueError("Central directory is outside of the file")
        cd = _Buffer(source.read(cdoffset, cdsize))

        # Parse central directory entries.
        self.files = {}
        for _ in range(entries):
            # Parse central directory header.
            cd.match(b"\x50\x4b\x01\x02")
            cd.move(4)
            flags = cd.number(2)
            if flags & 0x0001 != 0:
                raise ValueError(_ENCRYPTED_ERRMSG)
            if flags & 0x0008 != 0:
                raise ValueError("Data descriptor is not supported")
            if flags & 0x0020 != 0:
                raise ValueError("Compressed patched data is not supported")
            if flags & 0x0040 != 0:
                raise ValueError(_ENCRYPTED_ERRMSG)
            if flags & 0x0800 != 0:
                raise ValueError("UTF-8 is not supported")
            if flags & 0x2000 != 0:
                raise ValueError(_ENCRYPTED_ERRMSG)
            cd.number_match(2, 0, _COMPRESSED_ERRMSG)
            cd.move(4)
            crc32 = cd.number(4)
            fsize = cd.number(4)
            cd.number_match(4, fsize, _COMPRESSED_ERRMSG)
            fnamelen = cd.number(2)
            extralen = cd.number(2)
            fcommentlen = cd.number(2)
            cd.number_match(2, 0, _MULTIDISK_ERRMSG)
            cd.move(6)
            foffset = cd.number(4)
            fname = cd.read(fnamelen)
            extra_block = cd.read(extralen)
            fcomment = cd.read(fcommentlen)

            # Look for ZIP64 extended information extra data field.
            if fsize == 0xFFFFFFFF or foffset == 0xFFFFFFFF:
                extra = _Buffer(extra_block)
                while not extra.end():
                    extid = extra.number(2)
                    extsize = extra.number(2)
                    if extid == 0x0001:
                        if extsize not in (8, 16, 24, 28):
                            raise ValueError("Invalid ZIP64 extra data size")
                        fsize = extra.number(8)
                        if extsize >= 16:
                            extra.number_match(8, fsize, _COMPRESSED_ERRMSG)
                        if extsize >= 24:
                            foffset = extra.number(8)
                        if extsize >= 28:
                            extra.number_match(4, 0, _MULTIDISK_ERRMSG)
                        break
                    else:
                        extra.move(extsize)

            if foffset + fsize > source.size():
                raise ValueError("File is outside of the archive")
            if fname in self.files:
                raise ValueError(f"Duplicate file name {fname}")
            self.files[fname] = File(
                name=fname, offset=foffset, size=fsize, crc32=crc32, comment=fcomment
            )

        if not cd.end():
            raise ValueError("Central directory has trailing data")

    def __len__(self) -> int:
        """Return the number of files in the archive."""
        return len(self.files)

    def __iter__(self) -> Iterable[bytes]:
        """Return an iterator over file names in the archive."""
        return iter(self.files)

    def __getitem__(self, name: bytes) -> bytes:
        """Return the payload of the file with the given name."""
        if name not in self.files:
            raise KeyError(name)
        file = self.files[name]

        # Read a data block large enough to contain local file header
        # with maximum-sized extra field and payload.
        # Assume that file name and it's length are equal
        # to the corresponding values from the central directory.
        data = _Buffer(self.source.read(file.offset, file.size + 65565))
        data.match(b"\x50\x4b\x03\x04")
        data.move(24)
        data.move(len(file.name) + data.number(2))
        payload = data.read(file.size)

        if zlib.crc32(payload) != file.crc32:
            raise ValueError("CRC32 mismatch")
        return payload
