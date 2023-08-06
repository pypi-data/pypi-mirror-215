from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'A package to train AI models with no code.'
LONG_DESCRIPTION = 'This uses some amount of user intervention to to output AI models requiring no code from the side of the user.'

# Setting up
setup(
    name="generalized-model-trainer",
    version=VERSION,
    author="Ojasva Chaarag",
    author_email="<ojasva@chaarag.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'ai', 'ml', 'artificial intelligence', 'machine learning', 'ai model', 'ml model', 'no code', 'create model', 'create ai', 'create ml', 'create ai model', 'create ml model'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)