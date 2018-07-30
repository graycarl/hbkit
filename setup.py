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
    packages=['hbkit'],
    install_requires=['click>=5.0', 'requests>=2.0', 'future>=0.16',
                      'arrow>=0.12', 'configparser>=3.5'],
    extras_require=dict(dev=['mock', 'pytest']),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    entry_points={
        'console_scripts': [
            'hbkit=hbkit:cli'
        ]
    }
)
