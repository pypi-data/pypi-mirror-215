import setuptools
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="credit_card_info_generator",
    version="1.0",
    description="Credit Card Info Generator is a Python package designed to create realistic dummy credit card data. "
                "It's a handy tool for developers who need to test payment systems, verify eCommerce applications, "
                "or any situation where real credit card data is not necessary or desirable."
                "It supports a variety of card providers and generates corresponding credit card numbers, CVVs, "
                "and expiry dates.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Bellamy",
    author_email="bellamyy.blakee100@gmail.com",
    url="https://creditcardgenerator.app/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

