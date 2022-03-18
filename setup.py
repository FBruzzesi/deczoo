from setuptools import setup, find_packages

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
    "mkdocs==1.1",
    "mkdocs-material==4.6.3",
    "mkdocstrings==0.8.0",
    "mktestdocs==0.1.2",
]

dev_packages = test_packages + docs_packages

setup(
    name="deczoo",
    version="0.1.0",
    author="Francesco Bruzzesi",
    packages=find_packages(exclude=["notebooks", "docs", "tests"]),
    description="a zoo for decorators",
    install_requires=base_packages,
    extras_require={"optional": optional_packages, "dev": dev_packages},
)
