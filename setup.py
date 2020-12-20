import setuptools
from collections import OrderedDict

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywiktionary",
    version="0.2.a0.post0",
    author="Alessandro Mesti",
    author_email="mesti.alessandro@gmail.com",
    description="Python library to retrieve wiktionary word definitions for different languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests>=2,<3',
        'BeautifulSoup4>=4',
    ],
    project_urls=OrderedDict(
        (
            ("Code", "https://github.com/alessandrome/pywiktionary"),
        )
    ),
    packages=setuptools.find_packages(exclude=("*.tests", "*.tests.*", "tests.*", "tests")),
    keywords="wiktionary parser scraper word words multilingual",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
)