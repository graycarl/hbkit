import os
from typing import Iterator
import configparser


def find_root(path: str, max_depth=8) -> str | None:
    for _ in range(max_depth):
        if os.path.exists(os.path.join(path, '.git')):
            break
        path = os.path.dirname(path)
    else:
        return None
    return path


def iter_remotes_from_git_config(content: str) -> Iterator[str]:
    cp = configparser.ConfigParser()
    cp.read_string(content)
    for section in cp:
        if section.startswith('remote '):
            yield cp[section]['url']
