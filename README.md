# 自用命令行工具

[![Build Status](https://travis-ci.org/graycarl/hbkit.svg?branch=master)](https://travis-ci.org/graycarl/hbkit)

```bash
$ hbkit --help
Usage: hbkit [OPTIONS] COMMAND [ARGS]...

Options:
  --version      Print out current version.
  --config PATH  The config file path.  [default: ~/.config/hbkit/hbkit.ini]
  --help         Show this message and exit.

Commands:
  backup      Make a backup copy for file or directory.
  git         Tools for git.
  pi          Tools for Raspberry PI
  random      Generate random string.
  short       Shorten your url.
  time        Tools about date & time.
  watch-urls  Watch urls status.
```

## Setup Dev Environment

1. Create add active a virtualenv;
2. Run `pip install -e '.[dev]'` in root dir;
3. Run `py.test`;
