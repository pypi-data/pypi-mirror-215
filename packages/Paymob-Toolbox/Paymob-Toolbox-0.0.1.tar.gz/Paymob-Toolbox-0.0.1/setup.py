import codecs
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="Paymob-Toolbox",
    version='0.0.1',
    author="DjangoFam Team",
    author_email="mahmoud.nasser.abdulhamed11@gmail.com",
    description="A simple Python package that provides convenient access to the Paymob APIs from applications written in the Python language.",
    url="https://github.com/muhammedattif/Paymob",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['pypi', 'paymob', 'payment', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
