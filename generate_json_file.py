import os

from DataHandler.DataFormater import DataFormater
from Util.Util import Util

if __name__ == "__main__":
    # List your text files here

    current_directory = os.getcwd()
    directory = current_directory + '\\answers\\'
    text_files = Util.get_files_in_directory(directory)

    # Create parser instance
    parser = DataFormater()

    # Process files
    parser.process_files(text_files)

    # Save to JSON
    parser.save_to_json("catalyst_synthesis_qa_pairs.json")

    # Optionally get the QA pairs for further processing
    qa_pairs = parser.get_qa_pairs()
    print(f"Collected {len(qa_pairs)} QA pairs about catalyst synthesis.")