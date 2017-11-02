import os
import sys

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
)
# fix locale settings
# When runed by vscode python unittest extension, the locale
# environment value will lost. That will cause RuntimeError
# in python3.
os.environ.setdefault('LANG', 'en_US.UTF-8')
os.environ.setdefault('LC_CTYPE', 'en_US.UTF-8')
