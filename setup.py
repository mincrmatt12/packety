import os

from setuptools import setup

setup(
    name="packety",
    version="0.0.6a2",
    packages=["packety"],
    install_requires=["gevent"],

    author="mincrmatt12",
    description="Simple packet based networking, with a side of async",
    long_description=open("readme.rst").read() if os.path.exists("readme.rst") else "Readme is missing, please get git source or read pypi",
    keywords="networking packet async"
)