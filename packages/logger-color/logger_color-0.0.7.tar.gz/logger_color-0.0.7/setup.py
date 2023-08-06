"""Package setup"""

import pathlib

from setuptools import setup, find_packages  # type: ignore

import logger_color as package

VERSION = "0.0.7"
PACKAGE = package.__title__
PACKAGE_ = package.__title__.lower().replace("-", "_")  # PEP 503 normalization
ROOT = pathlib.Path(__file__).parent.resolve()
README = "README.rst"

if __name__ == "__main__":
    setup(
        name=PACKAGE_,
        packages=[PACKAGE_],
        package_data={PACKAGE_: ["py.typed"]},
        version=VERSION,
        description=package.__summary__,
        license=package.__license__,
        long_description=open(README).read(),
        long_description_content_type="text/x-rst",
        author=package.__author__,
        author_email=package.__email__,
        url=package.__url__,
        download_url=package.__download_url__,
        keywords="logging",
        python_requires=">=3.8",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Natural Language :: English",
        ],
    )
