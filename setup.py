from setuptools import setup


setup(
    name='hbkit',
    version='0.2',
    packages=['hbkit'],
    install_requires=['Click', 'requests'],
    entry_points={
        'console_scripts': [
            'hbkit=hbkit:cli'
        ]
    }
)
