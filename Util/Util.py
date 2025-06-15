from typing import List
import re
import os

class Util:
    @classmethod
    def save_string_to_file(cls, content: str, filename: str) -> None:
        """
        Saves the content of a string to a text file.

        Args:
            content (str): The string content to be saved.
            filename (str): The name of the file to save to (including .txt extension).

        Returns:
            None
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Content successfully saved to {filename}")
        except IOError as e:
            print(f"Error saving file: {e}")

    # Example usage:
    # save_string_to_file("Hello, this is some sample text.", "output.txt")

    @classmethod
    def filter_out_figure_captions(cls, strings: List[str]) -> List[str]:
        """
        Filters out strings that are figure captions, including:
        - Standard figure captions (Fig. 1, Figure 2, etc.)
        - Extended data figures (Extended Data Fig. 3)
        - Supplementary figures (Supplementary Fig. 4)
        - Variations with pipes, colons, or other separators (Fig. 1 | Description)
        - Parenthetical figure references ([Fig. S1])

        Args:
            strings: List of input strings to filter

        Returns:
            List of strings with figure captions removed
        """
        # Compile pattern for figure captions
        figure_pattern = re.compile(
            r'^(\s*'  # Optional whitespace at start
            r'('
            r'([A-Za-z]+\s+)*'  # Optional prefix words (Extended Data, Supplementary, etc.)
            r'(Fig(ure)?s?|Scheme|Table|Graphical Abstract)'  # Figure/scheme/table keywords
            r'([\s\-\.][A-Za-z]?)?'  # Optional sub-figure notation (Fig. 1a)
            r'\s*\d+'  # Figure number
            r'[\s\-\.:|\])]'  # Separators (space, -, ., :, |, ], ) etc.)
            r')'
            r'|'  # OR
            r'[\[\(]Fig(ure)?s?\s*\d+[\]\)]'  # Parenthetical/bracketed references
            r')',
            re.IGNORECASE
        )

        return [s for s in strings if not figure_pattern.search(s.strip())]

    @classmethod
    def filter_out_references(cls, strings: List[str]) -> List[str]:
        """
        Filters out strings that are academic references or citations, including:
        - Numbered references ([1], [1-3], [1,3,5])
        - Author-date citations (Smith et al., 2020)
        - Bibliography entries (1. Author Name...)
        - DOI references
        - Reference section headers

        Args:
            strings: List of input strings to filter

        Returns:
            List of strings with references removed
        """
        # Compile pattern for references
        reference_pattern = re.compile(
            r'^(\s*'  # Optional whitespace
            r'('
            r'(\[\d+[,\-\s\d]*\])'  # Numbered citations [1], [1,2], [1-3]
            r'|(\d+\.\s+[A-Z])'  # Bibliography entries (1. Author)
            r'|(references?\s*$)'  # Reference section header
            r'|(doi\s*:|https?://doi\.org/)'  # DOI references
            r'|([A-Z][a-z]+(\set\sal\.)?,\s*\d{4})'  # Author-date (Smith et al., 2020)
            r'|(^©\s)'  # Copyright notices
            r'|(^(received|accepted|published)\s)'  # Publication dates
            r')'
            r')',
            re.IGNORECASE
        )

        return [s for s in strings if not reference_pattern.search(s.strip())]

    @classmethod
    def save_strings_to_file(cls, strings, filename, separator='\n\n'):
        """
        Save an array of strings to a text file.

        Parameters:
        - strings: List of strings to be saved
        - filename: Name of the output file (can include path)
        - separator: String used to separate the strings (default is newline)

        Returns:
        - True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(separator.join(strings))
            print(f"Successfully saved {len(strings)} strings to {filename}")
            return True
        except PermissionError:
            print(f"Permission denied: Could not write to {filename}")
        except OSError as e:
            print(f"Error saving file {filename}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return False

    @classmethod
    def replace_slashes(cls, input_str):
        return input_str.replace('/', '_')

    @classmethod
    def replace_underscore(cls, input_str):
        return input_str.replace('_', '/')

    @classmethod
    def read_doi_paper_file(cls, file_path):
        """
        Reads a text file named after a DOI containing paper contents.

        Args:
            file_path (str): Path to the text file (DOI as filename)

        Returns:
            dict: A dictionary containing:
                - 'doi': The DOI extracted from filename
                - 'content': The full text content
                - 'paragraphs': List of paragraphs (split by empty lines)
        """

        try:
            # Extract DOI from filename (remove .txt extension)
            doi = os.path.basename(file_path).replace('.txt', '')

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Split into paragraphs (assuming paragraphs are separated by empty lines)
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

                return {
                    'doi': doi,
                    'content': content,
                    'paragraphs': paragraphs
                }

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    @classmethod
    def get_files_in_directory(cls, directory_path, include_subdirectories=False, file_extensions=None):
        """
        Get all files in a specified directory.

        Args:
            directory_path (str): Path to the directory to search
            include_subdirectories (bool): Whether to include files from subdirectories (default: False)
            file_extensions (list): Optional list of file extensions to filter by (e.g., ['.txt', '.pdf'])

        Returns:
            list: List of file paths found in the directory
        """
        file_list = []

        # Check if directory exists
        if not os.path.isdir(directory_path):
            raise ValueError(f"Directory does not exist: {directory_path}")

        # Walk through directory
        if include_subdirectories:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_extensions:
                        if any(file_path.lower().endswith(ext) for ext in file_extensions):
                            file_list.append(file_path)
                    else:
                        file_list.append(file_path)
        else:
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                if os.path.isfile(item_path):
                    if file_extensions:
                        if any(item_path.lower().endswith(ext) for ext in file_extensions):
                            file_list.append(item_path)
                    else:
                        file_list.append(item_path)

        return file_list

if __name__ == "__main__":
    # Assuming the file is in the same directory
    result = Util.read_doi_paper_file('C:\\Users\\Aobo\\Desktop\\10.1038_nature21672.txt')

    if result:
        print(f"DOI: {result['doi']}")
        print(f"Number of paragraphs: {len(result['paragraphs'])}")
        print("\nFirst paragraph:")
        print(result['paragraphs'][0])