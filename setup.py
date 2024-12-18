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
    install_requires=['click~=7.0', 'requests~=2.0',
                      'arrow~=1.0', 'configparser~=3.5', 'dnspython~=1.15'],
    extras_require=dict(dev=['mock', 'pytest', 'mypy']),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    require_python='>=3.6',
    entry_points={
        'console_scripts': [
            'hbkit=hbkit:cli'
        ]
    }
)
