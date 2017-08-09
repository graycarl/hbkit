from setuptools import setup
import hbkit


setup(
    name='hbkit',
    version=hbkit.__version__,
    packages=['hbkit'],
    install_requires=['Click', 'requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hbkit=hbkit:cli'
        ]
    }
)
