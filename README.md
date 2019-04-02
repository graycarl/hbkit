## my own command line tool

[![Build Status](https://travis-ci.org/graycarl/hbkit.svg?branch=master)](https://travis-ci.org/graycarl/hbkit)

Developed in Python3, also work smoothly in Python2 with python-future.

```bash
$ hbkit --help
Usage: hbkit [OPTIONS] COMMAND [ARGS]...

Options:
  --version      Print out current version.
  --config PATH  The config file path.  [default: ~/.config/hbkit/hbkit.ini]
  -v, --verbose  Print execution details.
  --help         Show this message and exit.

Commands:
  backup      Make a backup copy for file or directory.
  config      Commands about configuration management.
  dns         DNS Management Commands.
  git         Tools for git.
  ip          Tools about ip address.
  random      Generate random string.
  short       Shorten your url.
  time        Tools about date & time.
  watch-urls  Watch urls status.
```

## Setup Dev Environment

1. Create add active a virtualenv;
2. Run `pip install -e '.[dev]'` in root dir;
3. Run `py.test`;
