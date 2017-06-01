"""Backup simplified.

monsoon is a toolkit that simplifies the process of backing up databases. It
handles the backup process itself as well as upload and error notification.
"""

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="monsoon-cli",
    version="0.1.2",
    description="Backup made easy.",
    long_description=LONG_DESCRIPTION,
    url="https://github.ibm.com/apset/monsoon",
    author="Luiz Aoqui",
    author_email="laoqui@ca.ibm.com",
    license="IBM",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Database",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "monsoon=monsoon:main"
        ]
    }
)
