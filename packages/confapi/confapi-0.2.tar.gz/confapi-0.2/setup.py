# pylint: disable-all

from setuptools import setup, find_packages

setup(
    name="confapi",
    url="https://github.com/illini-motorsports/confapi",
    version=0.2,
    author="cmmeyer1800",
    author_email="collinmmeyer@gmail.com",
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=(find_packages(exclude="tests")),
    install_requires=["requests>=2.31.0", "PyYAML>=6.0"],
)
