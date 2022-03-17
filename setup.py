from setuptools import setup, find_packages

# base_packages = []
# test_packages = []

# all_packages = base_packages
# dev_packages = all_packages + test_packages

setup(
    name="deczoo",
    version="0.1.0",
    author="Francesco Bruzzesi",
    packages=find_packages(exclude=["notebooks", "docs"]),
    description="a zoo for decorators",
    # install_requires=base_packages,
    # extras_require={"dev": dev_packages},
)
