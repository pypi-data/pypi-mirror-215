"""Cache manager of traced repos.
"""
import os
import shutil
from pathlib import Path
from filelock import FileLock
from typing import Optional, Tuple
from dataclasses import dataclass, field

from ..utils import (
    execute,
    get_repo_info,
    report_critical_failure,
)
from ..constants import CACHE_DIR


def _split_git_url(url: str) -> Tuple[str, str]:
    """Split a Git URL into user name and repo name."""
    if url.endswith("/"):
        url = url[:-1]
        assert not url.endswith("/"), f"Unexpected URL: {url}"
    fields = url.split("/")
    user_name = fields[-2]
    repo_name = fields[-1]
    return user_name, repo_name


def _format_dirname(url: str, commit: str) -> str:
    user_name, repo_name = _split_git_url(url)
    return f"{user_name}-{repo_name}-{commit}"


_CACHE_CORRPUTION_MSG = "The cache may have been corrputed!"


@dataclass(frozen=True, eq=False)
class Cache:
    """Cache manager."""

    cache_dir: Path
    lock: FileLock = field(init=False, repr=False)

    def __post_init__(self):
        if not os.path.exists(self.cache_dir):
            self.cache_dir.mkdir()
        lock_path = self.cache_dir.with_suffix(".lock")
        object.__setattr__(self, "lock", FileLock(lock_path))

    def get(self, url: str, commit: str) -> Optional[Path]:
        """Get the path of a traced repo with URL ``url`` and commit hash ``commit``. Return None if no such repo can be found."""
        _, repo_name = _split_git_url(url)
        dirpath = self._format_dirpath(url, commit) / repo_name
        with self.lock:
            if dirpath.exists():
                return dirpath
            else:
                return None

    def store(self, src: Path) -> Path:
        """Store a traced repo at path ``src``. Return its path in the cache."""
        dirs = list(src.glob("*"))
        assert len(dirs) == 1, f"Unexpected number of directories in {src}"
        url, commit = get_repo_info(dirs[0])
        dirpath = self._format_dirpath(url, commit)
        if not dirpath.exists():
            with self.lock:
                with report_critical_failure(_CACHE_CORRPUTION_MSG):
                    shutil.copytree(src, dirpath)
                    # Prevent the cache from being modified accidentally.
                    execute(f"chmod -R a-w {dirpath}")
        _, repo_name = _split_git_url(url)
        return dirpath / repo_name

    def _format_dirpath(self, url: str, commit: str) -> Path:
        dirname = _format_dirname(url, commit)
        return self.cache_dir / dirname


cache = Cache(CACHE_DIR)
"""A global :class:`Cache` object managing LeanDojo's caching of traced repos (see :ref:`caching`).
"""
