import json
import re
from typing import List, Dict, Optional


class DataFormatter:
    """
    A class to parse catalyst synthesis questions and answers from text files,
    keeping the answer content intact, and save them to JSON format.
    """

    def __init__(self):
        """Initialize the parser with an empty list of QA pairs."""
        self.qa_pairs = []

    def extract_qa_from_file(self, file_path: str) -> Optional[Dict]:
        """
        Extract the complete question and answer about catalyst synthesis from a text file.

        Args:
            file_path: Path to the text file containing catalyst synthesis information.

        Returns:
            Dictionary containing the QA pair if successful, None otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Extract the question (from the "question:" section)
                question_match = re.search(
                    r'question:\s*\n\n(.*?)(?=\n\nreasoning:|\n\nanswer:|\n\n\[file content end\]|\Z)',
                    content,
                    re.DOTALL
                )

                # Extract the complete answer (everything after "answer:")
                answer_match = re.search(
                    r'answer:\s*\n\n(.*?)(?=\n\n\[file content end\]|\Z)',
                    content,
                    re.DOTALL
                )

                if not question_match or not answer_match:
                    print(f"Could not extract complete QA pair from {file_path}")
                    return None

                question = question_match.group(1).strip()
                answer = answer_match.group(1).strip()

                # Standardize the question if it's too generic
                if "Imagine you are a chemist" in question:
                    question = "What catalysts are synthesized and what are their synthesis procedures?"

                return {
                    "conversation": [{
                        "input": question,
                        "output": answer
                    }]
                }

        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return None

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


# Example usage
if __name__ == "__main__":
    # List your text files here
    text_files = [
        "10.1038_nature21672.txt",
        "10.1038_s41586-020-03130-6.txt",
        "10.1038_s41586-022-05251-6.txt",
        "10.1038_s41586-023-06060-1.txt",
        "10.1038_s41586-024-08483-w.txt",
        "10.1038_s41586-025-09068-x.txt"
    ]

    # Create parser instance
    parser = DataFormatter()

    # Process files
    parser.process_files(text_files)

    # Save to JSON
    parser.save_to_json("catalyst_synthesis_qa_pairs.json")

    # Optionally get the QA pairs for further processing
    qa_pairs = parser.get_qa_pairs()
    print(f"Collected {len(qa_pairs)} QA pairs about catalyst synthesis.")