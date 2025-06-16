import json
import re
from typing import List, Dict, Optional


class DataFormater:
    """
    A class to parse catalyst synthesis questions and answers from text files and save them to JSON format.

    Attributes:
        qa_pairs (List[Dict]): List of question-answer pairs in dictionary format
    """

    def __init__(self):
        """Initialize the parser with an empty list of QA pairs."""
        self.qa_pairs = []

    def extract_qa_from_file(self, file_path: str) -> Optional[Dict]:
        """
        Extract question and answer about catalyst synthesis from a single text file.

        Args:
            file_path: Path to the text file containing catalyst synthesis information.

        Returns:
            Dictionary containing the QA pair if successful, None otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Find the answer section
                answer_match = re.search(
                    r'answer:\s*\n\n(.*?)(?=\n\n\[file content end\]|\Z)',
                    content,
                    re.DOTALL
                )

                if not answer_match:
                    print(f"No answer section found in {file_path}")
                    return None

                answer_text = answer_match.group(1).strip()

                # Extract the synthesized catalysts section
                synthesized_match = re.search(
                    r'Synthesized Catalysts.*?\n(.*?)\n\n',
                    answer_text,
                    re.DOTALL
                )

                if not synthesized_match:
                    # Alternative pattern if "Synthesized Catalysts" isn't found
                    synthesized_match = re.search(
                        r'1\..*?Catalyst Synthesized.*?\n(.*?)\n\n',
                        answer_text,
                        re.DOTALL
                    )

                # Create the question and clean the answer
                question = "What catalysts are synthesized and what are their synthesis procedures?"
                answer = self._clean_answer_text(answer_text)

                if not answer:
                    print(f"No valid answer content found in {file_path}")
                    return None

                return {
                    "conversation": [{
                        "input": question,
                        "output": answer
                    }]
                }

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return None

    def _clean_answer_text(self, answer_text: str) -> str:
        """
        Clean up the answer text by removing unnecessary sections.

        Args:
            answer_text: Raw answer text from the file

        Returns:
            Cleaned answer text
        """
        # Remove any "Key Synthesis Features" or similar sections
        cleaned = re.sub(r'\*\*Key.*', '', answer_text, flags=re.DOTALL)
        cleaned = re.sub(r'\*\*Note.*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'\[.*?\]', '', cleaned)  # Remove any citation markers
        cleaned = cleaned.strip()
        return cleaned

    def process_files(self, file_paths: List[str]) -> None:
        """
        Process multiple text files to extract QA pairs.

        Args:
            file_paths: List of paths to text files
        """
        for file_path in file_paths:
            qa_pair = self.extract_qa_from_file(file_path)
            if qa_pair:
                self.qa_pairs.append(qa_pair)

    def save_to_json(self, output_path: str) -> None:
        """
        Save the collected QA pairs to a JSON file.

        Args:
            output_path: Path to save the JSON file
        """
        if not self.qa_pairs:
            print("No QA pairs to save.")
            return

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.qa_pairs, f, indent=2, ensure_ascii=False)
            print(f"Successfully saved {len(self.qa_pairs)} QA pairs to {output_path}")
        except Exception as e:
            print(f"Error saving to JSON: {str(e)}")

    def get_qa_pairs(self) -> List[Dict]:
        """
        Get the collected QA pairs.

        Returns:
            List of QA pair dictionaries
        """
        return self.qa_pairs