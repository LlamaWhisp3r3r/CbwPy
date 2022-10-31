import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "CbwPy",
    version = "1.0.0",
    author = "Nate Turner",
    author_email = "nathanturner270@gmail.com",
    description = ("API connection to Control By Web X410"),
    url = "https://github.com/NathanTurner270/CbwPy",
    packages=find_packages(include=['CbwPy', 'CbwPy.*']),
    long_description=read('README.md'),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
)