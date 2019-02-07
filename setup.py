from setuptools import setup

setup(
    name = 'azdevman',
    version = '0.0.1',
    packages = ['azdevman'],
    entry_points = {
        'console_scripts': [
            'azdevman = azdevman.main:cli'
        ]
    }
)
