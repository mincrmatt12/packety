from setuptools import setup

setup(
    name="packety",
    version="0.0.6a1",
    packages=["packety"],
    install_requires=["gevent"],

    author="mincrmatt12",
    description="Simple packet based networking, with a side of async",
    long_description=open("readme.rst").read(),
    keywords="networking packet async"
)