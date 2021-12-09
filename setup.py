import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('hbkit/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='hbkit',
    version=version,
    packages=['hbkit', 'hbkit.libs'],
    package_data={'hbkit': ['data/clash-template.yml']},
    install_requires=['click~=5.0', 'requests~=2.0', 'future~=0.16',
                      'arrow~=1.0', 'configparser~=3.5', 'dnspython~=1.15'],
    extras_require=dict(dev=['mock', 'pytest', 'python-language-server',
                             'flake8', 'autopep8']),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    entry_points={
        'console_scripts': [
            'hbkit=hbkit:cli'
        ]
    }
)
