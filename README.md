## Personal command line tool

[![Build Status](https://travis-ci.org/graycarl/hbkit.svg?branch=master)](https://travis-ci.org/graycarl/hbkit)

Work on python3 only.

```bash
Usage: hbkit [OPTIONS] COMMAND [ARGS]...

Options:
  --version      Print out current version.
  --config FILE  The config file path.  [default: ~/.config/hbkit/hbkit.ini]
  -v, --verbose  Print execution details.
  --help         Show this message and exit.

Commands:
  backup   Make a backup copy for file or directory.
  clash    Some tools about using clash
  config   Commands about configuration management.
  dns      DNS Management Commands.
  fs       FileSystem management tools.
  git      Tools for git.
  github   Tools about github.
  ip       Tools about ip address.
  mac      Tools for living in macOS.
  random   Generate random string.
  time     Tools about date & time.
  upgrade  Upgrade hbkit from github.
  yaml     Tools about parsing yaml files.
```

## Setup Dev Environment

1. Create add active a virtualenv;
2. Run `pip install -e '.[dev]'` in root dir;
3. Run `py.test`;
