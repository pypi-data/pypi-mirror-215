import re
class LaTeXDocumentReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_document(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
        return content

    def read_bibtex(self, bibtex_file_path):
        with open(bibtex_file_path, 'r') as bibtex_file:
            bibtex_content = bibtex_file.read()
        return bibtex_content

    def make_readable(self, content):
        # Perform necessary processing to make the content human-readable
        # For example, you can remove LaTeX commands or format the text

        # Replace LaTeX commands with empty strings
        content = re.sub(r'\\[a-zA-Z]+\{[^\}]*\}', '', content)

        # Replace multiple whitespaces with a single whitespace
        content = re.sub(r'\s+', ' ', content)

        # Return the processed content
        return content
