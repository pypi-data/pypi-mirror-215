import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="hrsii",
    version="0.0.1",
    url="https://github.com/khlaifiabilel/High-resolution-Satellite-Image-Indexes",
    license="MIT",
    author="KhlaifiaBilel",
    author_email="khlaifiabilel@icloud.com",
    description="High-resolution-Satellite-Image-Indexes",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    package_data={"hrsii": ["data/*.json"]},
    install_requires=[
        "dask>=2021.9.1",
        "earthengine-api",
        "eemont>=0.3.6",
        "matplotlib",
        "numpy",
        "pandas",
        "python-box>=6.0",
        "requests",
        "seaborn",
        "xarray",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
