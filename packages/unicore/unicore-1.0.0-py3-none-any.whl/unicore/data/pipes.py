from __future__ import annotations

from typing import Sequence, Optional, Callable, Any

from torchdata.datapipes.iter import IoPathFileLister, IoPathFileOpener, IoPathSaver, IterDataPipe
from torchdata.datapipes import functional_datapipe

from .file_io import PathManager


@functional_datapipe("list_files_by_unicore")
class UniCoreFileLister(IoPathFileLister):
    """
    See ``IoPathFileLister``.
    """

    def __init__(self, root: str | Sequence[str] | IterDataPipe, masks: str | list[str]) -> None:
        super().__init__(root, masks, pathmgr=PathManager)


@functional_datapipe("open_files_by_unicore")
class UniCoreFileOpener(IoPathFileOpener):
    """
    See ``IoPathFileOpener``.
    """

    def __init__(self, source_datapipe: IterDataPipe[str], mode: str = "r") -> None:
        super().__init__(source_datapipe, mode, pathmgr=PathManager)


@functional_datapipe("save_by_unicore")
class UniCoreSaver(IoPathSaver):
    """
    See ``UniCoreSaver``.
    """

    def __init__(
        self,
        source_datapipe: IterDataPipe[tuple[Any, bytes | bytearray | str]],
        mode: str = "w",
        filepath_fn: Optional[Callable] = None,
    ):
        super().__init__(source_datapipe, mode, filepath_fn, pathmgr=PathManager)
