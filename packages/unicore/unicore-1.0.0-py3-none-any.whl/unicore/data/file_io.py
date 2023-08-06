"""
Implements a path manager for UniCore using IoPath.
"""

from __future__ import annotations
from iopath.common.file_io import PathManagerFactory
from iopath.common.file_io import HTTPURLHandler, OneDrivePathHandler, PathHandler

from typing import Optional, Final

try:
    from detectron2.utils.file_io import Detectron2Handler
except ImportError:
    Detectron2Handler = None

import os

__all__ = ["PathManager"]


class EnvironHandler(PathHandler):
    """
    Resolve prefix, e.g. `datasets://`, to the path to the datasets directory.
    """

    def __init__(self, prefix: str, env: str, default: Optional[str] = None):
        value = os.environ.get(env, default)
        if value is None:
            raise ValueError(f"Environment variable {env} not defined!")

        self.PREFIX: Final = prefix
        self.LOCAL: Final = value

    def _get_supported_prefixes(self):
        return [self.PREFIX]

    def _get_local_path(self, path: str, **kwargs):
        name = path[len(self.PREFIX) :]
        return PathManager.get_local_path(self.LOCAL + name, **kwargs)

    def _open(self, path: str, mode="r", **kwargs):
        name = path[len(self.PREFIX) :]
        return PathManager.open(self.LOCAL + name, mode, **kwargs)


PathManager = PathManagerFactory.get(defaults_setup=False)
PathManager.register_handler(OneDrivePathHandler())
PathManager.register_handler(HTTPURLHandler())

if Detectron2Handler is not None:
    PathManager.register_handler(Detectron2Handler())

PathManager.register_handler(EnvironHandler("datasets://", "DETECTRON2_DATASETS", "datasets"))
PathManager.register_handler(EnvironHandler("cache://", "UNIPERCEPT_CACHE", "cache"))
PathManager.register_handler(EnvironHandler("output://", "UNIPERCEPT_OUTPUT", "output"))
