from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
VERSION = "0.0.0"
DESCRIPTION = "Python project for Fxopen Broker"
LONG_DESCRIPTION = open("README.md", encoding="utf-8").read()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="fxopenpy",
    version=VERSION,
    author="Krishna Khatiwada",
    author_email="krishna.khatiwada187@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pandas", "python-dotenv", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "repository": "https://github.com/KrishnaInvestment/fxopenpy",
    },
)