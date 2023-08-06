from __future__ import annotations

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_entry_point

datas, hiddenimports = collect_entry_point("comicapi.archiver")
datas += collect_data_files("comicapi.data")
