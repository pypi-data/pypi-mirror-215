# PyDuplicate

[![PyPI Downloads](https://img.shields.io/pypi/dm/PyDuplicate.svg?label=PyPI%20downloads)](
https://pypi.org/project/PyDuplicate/)
[![Stack Overflow](https://img.shields.io/badge/stackoverflow-Ask%20questions-blue.svg)](
https://stackoverflow.com/questions/tagged/PyDuplicate)
[![Nature Paper](https://img.shields.io/badge/Article-Duplicate-Finder--blue)](
https://publishup.uni-potsdam.de/opus4-ubp/frontdoor/deliver/index/docId/48913/file/koumarelas_diss.pdf)


PyDuplicate is a Python package that provides functionality for detecting and identifying duplicates within a given dataset. 
It offers a bunch of functions to search for duplicate elements, making it easy to identify and handle duplicate entries efficiently.

- **Source code:** https://github.com/JeanBertinR/PyDuplicate
- **Bug reports:** https://github.com/JeanBertinR/PyDuplicate/issues
- **Report a security vulnerability:** https://tidelift.com/docs/security

## Requirements

- Python 3.x
- Levenshtein

## Installation

You can install the `PyDuplicate` package using `pip`. Here's the installation command from your terminal:

```shell
pip install PyDuplicate
```
Make sure you have Python and pip installed on your system before running this command.
After the installation, you can import the package in your Python code using the following line:
```python
import PyDuplicate
```
That's all it takes to install the package and import it into your project.

## Usage

### Importing the SimilarityScorer module

`SimilarityScorer` has been designed to calculate a similarity score between two sets of character strings.
To begin, import the package by installing it using pip and importing the `SimilarityScorer` class in your Python script or interactive session:

```python
from PyDuplicate import SimilarityScorer
```

### Instantiating the SimilarityScorer
Create an instance of the `SimilarityScorer` class:

```python
scorer = SimilarityScorer()
```

### Calculating the Similarity Score
Use the `similarity_score` method of the `SimilarityScorer` instance to calculate the similarity score between two sets of strings:
```python
score = scorer.similarity_score(str_tuple_1, str_tuple_2)
```

### Importance and Applications
The String Similarity Scorer function has several applications across various domains, including:

Text Matching: It can be used for comparing and matching textual data, such as finding duplicate entries in a database or identifying similar documents.

Data Cleansing: It aids in data preprocessing tasks by detecting and handling similar or duplicate records, improving data quality.

Natural Language Processing (NLP): The similarity score can be used as a feature in NLP tasks like text classification, information retrieval, and recommendation systems.

Fuzzy String Matching: The function incorporates fuzzy matching techniques to handle slight variations and inconsistencies in the input strings.
### Contributing
Contributions are welcome! If you have any suggestions or find any issues, please open an issue or submit a pull request.

### License
This project is licensed under the GPL v3 License.