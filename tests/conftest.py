import os

# fix locale settings
# When runed by vscode python unittest extension, the locale
# environment value will lost. That will cause RuntimeError
# in python3.
os.environ.setdefault('LANG', 'en_US.UTF-8')
os.environ.setdefault('LC_CTYPE', 'en_US.UTF-8')
