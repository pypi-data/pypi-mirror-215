from __future__ import annotations

import io
import logging
import os
import pathlib
import shutil
import tarfile
import tempfile
import time
from typing import cast
from typing import IO

from comicapi.archivers import Archiver

logger = logging.getLogger(__name__)


class TarArchiver(Archiver):

    """TAR implementation"""

    def __init__(self) -> None:
        super().__init__()
        # tar archives take filenames literally `./ComicInfo.xml` is not `ComicInfo.xml`
        self.path_norm: dict[str, str] = {}

    # @todo: Implement Comment? tar files do not have native comments
    def get_comment(self) -> str:
        return ""

    def set_comment(self, comment: str) -> bool:
        return False

    def read_file(self, archive_file: str) -> bytes:
        archive_file = str(pathlib.PurePosixPath(archive_file))
        if not self.path_norm:
            self.get_filename_list()
        if archive_file in self.path_norm:
            archive_file = self.path_norm[archive_file]

        try:
            with tarfile.TarFile(self.path, mode="r", encoding="utf-8") as tf:
                with cast(IO[bytes], tf.extractfile(archive_file)) as file:
                    data = file.read()
        except (tarfile.TarError, OSError) as e:
            logger.error("Error reading tar archive [%s]: %s :: %s", e, self.path, archive_file)
            raise
        return data

    def remove_file(self, archive_file: str) -> bool:
        return self.rebuild([archive_file])

    def write_file(self, archive_file: str, data: bytes) -> bool:
        # At the moment, no other option but to rebuild the whole
        # archive w/o the indicated file. Very sucky, but maybe
        # another solution can be found
        files = self.get_filename_list()
        if archive_file in files:
            if not self.rebuild([archive_file]):
                return False

        try:
            archive_file = str(pathlib.PurePosixPath(archive_file))
            # now just add the archive file as a new one
            with tarfile.TarFile(self.path, mode="a", encoding="utf-8") as tf:
                tfi = tarfile.TarInfo(archive_file)
                tfi.size = len(data)
                tfi.mtime = int(time.time())
                tf.addfile(tfi, io.BytesIO(data))
            return True
        except (tarfile.TarError, OSError) as e:
            logger.error("Error writing tar archive [%s]: %s :: %s", e, self.path, archive_file)
            return False

    def get_filename_list(self) -> list[str]:
        try:
            with tarfile.TarFile(self.path, mode="r", encoding="utf-8") as tf:
                namelist = []
                for name in tf.getnames():
                    new_name = pathlib.PurePosixPath(name)
                    namelist.append(str(new_name))
                    self.path_norm[str(new_name)] = name

            return namelist
        except (tarfile.TarError, OSError) as e:
            logger.error("Error listing files in tar archive [%s]: %s", e, self.path)

            return []

    def rebuild(self, exclude_list: list[str]) -> bool:
        """tar helper func

        This recreates the tar archive, without the files in the exclude_list
        """
        try:
            with tarfile.TarFile(
                fileobj=tempfile.NamedTemporaryFile(dir=os.path.dirname(self.path), delete=False),
                mode="w",
                encoding="utf-8",
            ) as tout:
                with tarfile.TarFile(self.path, mode="r", encoding="utf-8") as tin:
                    for item in tin.getmembers():
                        buffer = tin.extractfile(item)
                        if str(pathlib.PurePosixPath(item.name)) not in exclude_list:
                            tout.addfile(item, buffer)

                # replace with the new file
                self.path.unlink(missing_ok=True)
                tout.close()  # Required on windows

                shutil.move(str(tout.name), self.path)

        except (OSError, tarfile.TarError) as e:
            logger.error("Error rebuilding tar file [%s]: %s", e, self.path)
            return False
        return True

    def copy_from_archive(self, other_archive: Archiver) -> bool:
        # Replace the current tar with one copied from another archive
        try:
            with tarfile.TarFile(self.path, mode="w", encoding="utf-8") as tout:
                for fname in other_archive.get_filename_list():
                    data = other_archive.read_file(fname)
                    if data is not None:
                        # All archives should use `/` as the directory separator
                        tfi = tarfile.TarInfo(str(pathlib.PurePosixPath(fname)))
                        tfi.size = len(data)
                        tfi.mtime = int(time.time())
                        tout.addfile(tfi, io.BytesIO(data))

        except Exception as e:
            logger.error("Error while copying to tar archive [%s]: from %s to %s", e, other_archive.path, self.path)
            return False
        else:
            return True

    def is_writable(self) -> bool:
        """
        Retuns True if the current archive is writeable
        Should always return a boolean. Failures should return False.
        """
        return True

    def extension(self) -> str:
        """
        Returns the extension that this archiver should use eg ".cbz".
        Should always return a string. Failures should return the empty string.
        """
        return ".cbt"

    def name(self) -> str:
        """
        Returns the name of this archiver for display purposes eg "CBZ".
        Should always return a string. Failures should return the empty string.
        """
        return "TAR"

    @classmethod
    def is_valid(cls, path: pathlib.Path) -> bool:
        """
        Returns True if the given path can be opened by this archiver.
        Should always return a boolean. Failures should return False.
        """
        return tarfile.is_tarfile(path)
