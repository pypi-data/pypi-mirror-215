import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='latex-document-reader',
    version='1.0.1',
    author='Anıl ÖZ',
    author_email='anil.oz@icloud.com',
    description='A Python library for reading LaTeX documents and processing BibTeX files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ozanil/LaTeXDocumentReader.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='latex document reader bibtex',
    python_requires='>=3.6',
)
