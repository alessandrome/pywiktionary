import setuptools
from collections import OrderedDict

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywiktionary",
    version="0.0.a1",
    author="Alessandro Mesti",
    author_email="mesti.alessandro@gmail.com",
    description="Python library to retrieve wiktionary word definitions for different languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls=OrderedDict(
        (
            ("Code", "https://github.com/alessandrome/pywiktionary"),
        )
    ),
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers"
    ],
)