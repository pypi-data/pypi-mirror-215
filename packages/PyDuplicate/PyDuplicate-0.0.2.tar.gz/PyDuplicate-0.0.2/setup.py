from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Python functions for Efficient duplicate detection'
LONG_DESCRIPTION = 'Provides efficient and intuitive functionality for detecting and removing duplicates within a given dataset'

# Setting up
setup(
    name="PyDuplicate",
    version=VERSION,
    author="Jean BERTIN",
    author_email="<jeanbertin.ensam@gmail.com>",
    licence='GPL-3.0',
    description=DESCRIPTION,
    url="https://github.com/JeanBertinR/PyDuplicate",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['difflib', 'fuzzywuzzy', 'numpy'],
    keywords=['Duplicate detection', 'Efficient duplicate search'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
