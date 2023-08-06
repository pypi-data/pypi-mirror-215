from setuptools import setup, find_packages

setup(
    name='SkyScribe',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'skyscribe = skyscribe:cli',
        ],
    },
)
