from setuptools import setup, find_packages
import pathlib

base_packages = ["chime>=0.6.0"]
optional_packages = ["rich>=12.0.0"]

test_packages = [
    "black>=21.12b0",
    "flake8>=4.0.1",
    "interrogate>=1.5.0",
    "pre-commit>=2.15.0",
    "pytest>=6.0.0",
]

docs_packages = [
    "mkdocs==1.2.3",
    "mkdocs-material==4.6.3",
    "mkdocstrings==0.18.1",
    "mktestdocs==0.1.2",
]

dev_packages = test_packages + docs_packages

all_packages = dev_packages + base_packages + optional_packages

setup(
    name="deczoo",
    version="0.1.0",
    author="Francesco Bruzzesi",
    packages=find_packages(exclude=["notebooks", "docs"]),
    description="a zoo for decorators",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://fbruzzesi.github.io/deczoo/",
    project_urls={
        "Documentation": "https://fbruzzesi.github.io/deczoo/",
        "Source Code": "https://github.com/FBruzzesi/deczoo",
        "Issue Tracker": "https://github.com/FBruzzesi/deczoo/issues",
    },
    license_files=("LICENSE",),
    install_requires=base_packages,
    extras_require={
        "all": all_packages,
        "optional": optional_packages,
        "dev": dev_packages,
    },
)
