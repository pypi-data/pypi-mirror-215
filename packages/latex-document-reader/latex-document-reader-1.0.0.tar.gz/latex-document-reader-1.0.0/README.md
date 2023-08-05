# LaTeX Document Reader

[![PyPI version](https://badge.fury.io/py/LaTeXDocumentReader.svg)](https://badge.fury.io/py/LaTeXDocumentReader)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python library for reading LaTeX documents and processing BibTeX files.

## Installation

You can install the library using pip:

```shell
pip install latex-document-reader
```

## Usage
Reading LaTeX Documents
To read a LaTeX document, create an instance of the LaTeXDocumentReader class, passing the file path of the document as a parameter. Then, use the read_document method to retrieve the content of the document.

```python
from latex_document_reader import LaTeXDocumentReader

# Create an instance of LaTeXDocumentReader
document_reader = LaTeXDocumentReader('path/to/your/document.tex')

# Read the LaTeX document
content = document_reader.read_document()

# Print the content
print(content)
```

## Reading BibTeX Files
To process a BibTeX file, use the read_bibtex method of the LaTeXDocumentReader class, passing the file path of the BibTeX file as a parameter.

```python
from latex_document_reader import LaTeXDocumentReader

# Create an instance of LaTeXDocumentReader
document_reader = LaTeXDocumentReader('path/to/your/document.tex')

# Read a BibTeX file
bibtex_content = document_reader.read_bibtex('path/to/your/references.bib')

# Print the BibTeX content
print(bibtex_content)
```

## Making the File Human-Readable
The library also provides a make_readable method that can be used to process the content of a LaTeX document or any other text and make it human-readable. You can customize the method according to your specific requirements.

```python
from latex_document_reader import LaTeXDocumentReader

# Create an instance of LaTeXDocumentReader
document_reader = LaTeXDocumentReader('path/to/your/document.tex')

# Read the LaTeX document
content = document_reader.read_document()

# Make the content human-readable
readable_content = document_reader.make_readable(content)

# Print the human-readable content
print(readable_content)
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


