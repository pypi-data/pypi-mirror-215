from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="dowell-permutation",
    version="0.1.1",
    description="Dowell Permutation API Python Libray",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dowell-permutation.readthedocs.io/en/latest/",
    author='Dennis RK.',
    license="MIT",
    packages=["permutation"],
    include_package_data=True,
    install_requires=["requests"]
)