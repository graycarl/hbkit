import os
import configparser


def find_root(path, max_depth=8):
    for i in range(max_depth):
        if os.path.exists(os.path.join(path, '.git')):
            break
        path = os.path.dirname(path)
    else:
        return None
    return path


def iter_remotes_from_git_config(content):
    cp = configparser.ConfigParser()
    cp.read_string(content)
    for section in cp:
        if section.startswith('remote '):
            yield cp[section]['url']
