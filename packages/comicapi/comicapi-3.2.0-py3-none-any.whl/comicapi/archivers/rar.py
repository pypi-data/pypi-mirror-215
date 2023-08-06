from __future__ import annotations

import logging
import os
import pathlib
import platform
import shutil
import subprocess
import tempfile
import time
from typing import TypeVar

from comicapi.archivers import Archiver

try:
    import rarfile

    rar_support = True
except ImportError:
    rar_support = False


logger = logging.getLogger(__name__)

if not rar_support:
    logger.error("rar unavailable")


RSelf = TypeVar("RSelf", bound="RarArchiver")


class RarArchiver(Archiver):
    """RAR implementation"""

    enabled = rar_support
    exe = "rar"

    def __init__(self) -> None:
        super().__init__()

        # windows only, keeps the cmd.exe from popping up
        if platform.system() == "Windows":
            self.startupinfo = subprocess.STARTUPINFO()  # type: ignore
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # type: ignore
        else:
            self.startupinfo = None

    def get_comment(self) -> str:
        rarc = self._get_rar_obj()
        return (rarc.comment if rarc else "") or ""

    def set_comment(self, comment: str) -> bool:
        if rar_support and self._exe:
            try:
                # write comment to temp file
                with tempfile.TemporaryDirectory() as tmp_dir:
                    tmp_file = pathlib.Path(tmp_dir) / "rar_comment.txt"
                    tmp_file.write_text(comment, encoding="utf-8")

                    working_dir = os.path.dirname(os.path.abspath(self.path))

                    # use external program to write comment to Rar archive
                    proc_args = [
                        self._exe,
                        "c",
                        f"-w{working_dir}",
                        "-c-",
                        f"-z{tmp_file}",
                        str(self.path),
                    ]
                    subprocess.run(
                        proc_args,
                        startupinfo=self.startupinfo,
                        stdout=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        check=True,
                    )

                if platform.system() == "Darwin":
                    time.sleep(1)
            except (subprocess.CalledProcessError, OSError) as e:
                logger.exception("Error writing comment to rar archive [%s]: %s", e, self.path)
                return False
            else:
                return True
        else:
            return False

    def read_file(self, archive_file: str) -> bytes:
        rarc = self._get_rar_obj()
        if rarc is None:
            return b""

        tries = 0
        while tries < 7:
            try:
                tries = tries + 1
                data: bytes = rarc.open(archive_file).read()
                entries = [(rarc.getinfo(archive_file), data)]

                if entries[0][0].file_size != len(entries[0][1]):
                    logger.info(
                        "Error reading rar archive [file is not expected size: %d vs %d]  %s :: %s :: tries #%d",
                        entries[0][0].file_size,
                        len(entries[0][1]),
                        self.path,
                        archive_file,
                        tries,
                    )
                    continue

            except OSError as e:
                logger.error("Error reading rar archive [%s]: %s :: %s :: tries #%d", e, self.path, archive_file, tries)
                time.sleep(1)
            except Exception as e:
                logger.error(
                    "Unexpected exception reading rar archive [%s]: %s :: %s :: tries #%d",
                    e,
                    self.path,
                    archive_file,
                    tries,
                )
                break

            else:
                # Success. Entries is a list of of tuples:  ( rarinfo, filedata)
                if len(entries) == 1:
                    return entries[0][1]

                raise OSError

        raise OSError

    def remove_file(self, archive_file: str) -> bool:
        if self._exe:
            # use external program to remove file from Rar archive
            result = subprocess.run(
                [self._exe, "d", "-c-", self.path, archive_file],
                startupinfo=self.startupinfo,
                stdout=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if platform.system() == "Darwin":
                time.sleep(1)
            if result.returncode != 0:
                logger.error(
                    "Error removing file from rar archive [exitcode: %d]: %s :: %s",
                    result.returncode,
                    self.path,
                    archive_file,
                )
                return False
            return True
        else:
            return False

    def write_file(self, archive_file: str, data: bytes) -> bool:
        if self._exe:
            archive_path = pathlib.PurePosixPath(archive_file)
            archive_name = archive_path.name
            archive_parent = str(archive_path.parent).lstrip("./")

            # use external program to write file to Rar archive
            result = subprocess.run(
                [self._exe, "a", f"-si{archive_name}", f"-ap{archive_parent}", "-c-", "-ep", self.path],
                input=data,
                startupinfo=self.startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if platform.system() == "Darwin":
                time.sleep(1)
            if result.returncode != 0:
                logger.error(
                    "Error writing rar archive [exitcode: %d]: %s :: %s", result.returncode, self.path, archive_file
                )
                return False
            else:
                return True
        else:
            return False

    def get_filename_list(self) -> list[str]:
        rarc = self._get_rar_obj()
        tries = 0
        if rar_support and rarc:
            while tries < 7:
                try:
                    tries = tries + 1
                    namelist = []
                    for item in rarc.infolist():
                        if item.file_size != 0:
                            namelist.append(item.filename)

                except OSError as e:
                    logger.error("Error listing files in rar archive [%s]: %s :: attempt #%d", e, self.path, tries)
                    time.sleep(1)

                else:
                    return namelist
        return []

    def copy_from_archive(self, other_archive: Archiver) -> bool:
        """Replace the current archive with one copied from another archive"""
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = pathlib.Path(tmp_dir)
                rar_cwd = tmp_path / "rar"
                rar_cwd.mkdir(exist_ok=True)
                rar_path = (tmp_path / self.path.name).with_suffix(".rar").absolute()

                for filename in other_archive.get_filename_list():
                    (rar_cwd / filename).parent.mkdir(exist_ok=True, parents=True)
                    data = other_archive.read_file(filename)
                    if data is not None:
                        with open(rar_cwd / filename, mode="w+b") as tmp_file:
                            tmp_file.write(data)
                result = subprocess.run(
                    [self._exe, "a", "-r", "-c-", str(rar_path), "."],
                    cwd=rar_cwd.absolute(),
                    startupinfo=self.startupinfo,
                    stdout=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if result.returncode != 0:
                    logger.error("Error while copying to rar archive [exitcode: %d]: %s", result.returncode, self.path)
                    return False

                self.path.unlink(missing_ok=True)
                shutil.move(str(rar_path), self.path)
        except Exception as e:
            logger.exception("Error while copying to rar archive [%s]: from %s to %s", e, other_archive.path, self.path)
            return False
        else:
            return True

    def is_writable(self) -> bool:
        return bool(
            self._exe and (shutil.which(self._exe) or os.path.exists(self._exe)) and not self._exe.endswith("unrar")
        )

    def extension(self) -> str:
        return ".cbr"

    def name(self) -> str:
        return "RAR"

    @classmethod
    def is_valid(cls, path: pathlib.Path) -> bool:
        if rar_support:
            return rarfile.is_rarfile(str(path))
        return False

    @classmethod
    def open(cls: type[RSelf], path: pathlib.Path, exe: str = "") -> RSelf:
        archiver = super().open(path, exe)
        archiver._check_exe()

        return archiver

    def _check_exe(self) -> None:
        if not self._exe:  # ignore empty
            return

        abs_path = shutil.which(self.exe)  # get absolute path if it exists in the path
        is_unrar = "unrar" in os.path.basename(self._exe)
        if os.path.dirname(self._exe):  # if it is a relative path get the absolute path
            self._exe = os.path.abspath(self._exe)

        if is_unrar:  # guess rar path from provided path
            rar = os.path.join(os.path.dirname(self._exe), os.path.basename(self._exe).replace("unrar", "rar"))
            unrar = self._exe
        else:
            rar = self._exe
            unrar = os.path.join(os.path.dirname(self._exe), os.path.basename(self._exe).replace("rar", "unrar"))

        if rar == self.exe or rar == abs_path:  # if the provided value is "rar" or the absolute path to "rar" return
            return

        if shutil.which(rar):  # If the given rar ("/path/to/rar" or "rar2") is executable return
            self._exe = rar
            return

        if shutil.which(unrar):  # As a last resort use the provided unrar
            self._exe = unrar
            return
        else:
            pass  # no valid rar or unrar found. Go with the default

    def _get_rar_obj(self) -> rarfile.RarFile | None:
        if rar_support:
            # rar is a valid unrar
            rarfile.UNRAR_TOOL = self._exe
            try:
                rarc = rarfile.RarFile(str(self.path))
            except (OSError, rarfile.RarFileError) as e:
                logger.error("Unable to get rar object [%s]: %s", e, self.path)
            else:
                return rarc

        return None
