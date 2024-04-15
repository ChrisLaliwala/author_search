from setuptools import setup

setup(
    name="author_search",
    version="0.0.1",
    description="author search utility command line utility",
    maintainer="Chris Laliwala",
    maintainer_email="claliwal@andrew.cmu.edu",
    license="MIT",
    packages=["author_search"],
    install_requires=[
        "click",
        "requests",
        "python",
    ],
    entry_points={"console_scripts": ["author_search = author_search.main:main"]},
    long_descript="""
    This package contains a command line utility that allows users to search
    for authors using keywords.
    """,
)
