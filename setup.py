from setuptools import setup

setup(
    name="author_search",
    version="0.0.1",
    description="author search utility command line utility",
    maintainer="Chris Laliwala",
    maintainer_email="claliwal@andrew.cmu.edu",
    license="MIT",
    packages=["author_search"],
    entry_points={"console_scripts": ["author_search = author_search.main:main"]},
    long_descript="""\
author command line utility
============================""",
)