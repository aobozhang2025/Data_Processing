import os
from typing import Dict, List, Optional, Union
from pdfplumber import PDF
import warnings


class TextPDFParser:
    """
    A focused PDF parser class that extracts text content with structure using pdfplumber.

    Features:
    - Extract raw text (combined or page-by-page)
    - Extract structured text with formatting and positioning
    - Preserve document structure (headings, paragraphs)
    - Handle multi-column layouts
    - Access font information
    """

    def __init__(self, pdf_path: str):
        """
        Initialize the PDF parser with a PDF file path.

        Args:
            pdf_path (str): Path to the PDF file to parse
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        self.pdf_path = pdf_path
        self._pdf = PDF.open(pdf_path)
        self.metadata = self._pdf.metadata
        self.num_pages = len(self._pdf.pages)

    def extract_text(self, combine: bool = True) -> Union[str, Dict[int, str]]:
        """
        Extract text from the PDF.

        Args:
            combine (bool): If True, returns combined text as string.
                           If False, returns dict with page numbers as keys.

        Returns:
            Union[str, Dict[int, str]]: Either combined text or page-wise text
        """
        if combine:
            text = ""
            for page in self._pdf.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        else:
            page_texts = {}
            for i, page in enumerate(self._pdf.pages):
                page_texts[i + 1] = page.extract_text()
            return page_texts

    def extract_structured_text(self) -> List[Dict]:
        """
        Extract structured text with formatting and positioning information.

        Returns:
            List[Dict]: A list of dictionaries containing structured text elements
                        with their properties (text, coordinates, font, etc.)
        """
        structured_text = []

        for page_num, page in enumerate(self._pdf.pages):
            words = page.extract_words(
                x_tolerance=1,
                y_tolerance=1,
                keep_blank_chars=False,
                use_text_flow=True,
                extra_attrs=["fontname", "size", "object_type"]
            )

            for word in words:
                # Get font size with default fallback
                font_size = round(float(word.get("size", 10)), 2)  # Default to 10 if size not available

                structured_text.append({
                    "page": page_num + 1,
                    "text": word.get("text", ""),
                    "x0": round(float(word.get("x0", 0)), 2),
                    "y0": round(float(word.get("top", 0)), 2),
                    "x1": round(float(word.get("x1", 0)), 2),
                    "y1": round(float(word.get("bottom", 0)), 2),
                    "font": {
                        "name": word.get("fontname", "unknown"),
                        "size": font_size,
                        "bold": "bold" in str(word.get("fontname", "")).lower(),
                        "italic": "italic" in str(word.get("fontname", "")).lower(),
                    },
                    "type": word.get("object_type", "text"),
                })

        return structured_text

    def extract_paragraphs_as_text(self) -> List[str]:
        """
        Extract all paragraphs from the PDF as a list of strings in reading order,
        properly handling paragraphs that span across multiple pages.

        Returns:
            List[str]: Array of paragraph texts ordered by page number and vertical position,
                      with cross-page paragraphs kept intact.
        """
        paragraphs = []
        current_para = []
        prev_y = None
        prev_page_bottom = None

        for page_num, page in enumerate(self._pdf.pages):
            words = page.extract_words(
                x_tolerance=1,
                y_tolerance=1,
                keep_blank_chars=False,
                use_text_flow=True
            )

            # Get page dimensions to detect bottom of page
            page_height = page.height
            current_page_top = words[0]["top"] if words else 0

            for word in words:
                # Initialize prev_y if first word of document
                if prev_y is None:
                    prev_y = word["top"]

                # Calculate vertical movement
                vertical_gap = word["top"] - prev_y

                # Check for new paragraph if:
                # 1. Significant vertical gap (1.5x font size), AND
                # 2. Not continuing from previous page bottom
                if (abs(vertical_gap) > word.get("size", 10) * 1.5 and
                        not (prev_page_bottom and abs(word["top"] - current_page_top) < word.get("size", 10) * 1.5)):

                    if current_para:
                        paragraphs.append(" ".join(current_para))
                        current_para =[]

                current_para.append(word["text"])
                prev_y = word["top"]

            # Check if paragraph continues to next page
            if current_para:
                last_word = words[-1] if words else None
                if last_word and (last_word["bottom"] > page_height - 20):  # 20 is tolerance near page bottom
                    prev_page_bottom = last_word["bottom"]
                else:
                    paragraphs.append(" ".join(current_para))
                    current_para = []
                    prev_page_bottom = None

                # Add any remaining text from the last paragraph
        if current_para:
            paragraphs.append(" ".join(current_para))

        return paragraphs

    def close(self):
        """Close the PDF file and release resources."""
        self._pdf.close()

    def __enter__(self):
        """Support for context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure PDF is closed when exiting context."""
        self.close()


# Example usage
if __name__ == "__main__":
    # Using context manager for automatic resource cleanup
    with TextPDFParser("C:\\Users\\Aobo\\Desktop\\test.pdf") as parser:
        # Extract raw text
        raw_text = parser.extract_text()
        print(f"Extracted {len(raw_text)} characters of text")

        # Extract structured text
        structured_text = parser.extract_structured_text()
        print(f"Extracted {len(structured_text)} text elements with structure")

        # Extract by paragraphs
        paragraphs = parser.extract_paragraphs_as_text()
        for paragraph in paragraphs:
            print(paragraph)