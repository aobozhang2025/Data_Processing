from typing import List
import re


class CatalystSynthesisExtractor:
    """
    A class to filter catalyst synthesis descriptions from an array of strings
    using predefined keywords.
    """

    def __init__(self):
        """
        Initialize the filter with synthesis keywords.
        """
        self.synthesis_keywords = [
            "synthesis", "preparation", "fabrication", "prepared by",
            "synthesized by", "was prepared", "were prepared", "catalyst preparation",
            "synthesis method", "preparation method", "fabrication process",
            "was synthesized", "were synthesized", "prepared via", "synthesized via",
            "prepared using", "synthesized using", "prepared through",
            "synthesized through", "prepared according to", "synthesized according to",
            "synthesis procedure", "preparation procedure", "fabrication procedure",
            "synthesis route", "preparation route", "fabrication route",
            "synthesis protocol", "preparation protocol", "fabrication protocol",
            "impregnation", "calcination", "precipitation", "hydrothermal",
            "sol-gel", "co-precipitation", "incipient wetness", "dry impregnation"
        ]

        # Create a regular expression pattern for case-insensitive matching
        self.pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, self.synthesis_keywords)) + r')\b',
            re.IGNORECASE
        )

    def filter_strings(self, strings: List[str]) -> List[str]:
        """
        Filter a list of strings to find those containing synthesis keywords.

        Args:
            strings (List[str]): List of strings to filter

        Returns:
            List[str]: Strings containing synthesis keywords
        """
        return [s for s in strings if self.pattern.search(s)]

    def count_keywords_in_string(self, string: str) -> int:
        """
        Count how many synthesis keywords appear in a string.

        Args:
            string (str): The string to analyze

        Returns:
            int: Number of unique synthesis keywords found
        """
        matches = self.pattern.findall(string.lower())
        return len(set(matches))

    def rank_strings_by_relevance(self, strings: List[str]) -> List[tuple]:
        """
        Rank strings by the number of synthesis keywords they contain.

        Args:
            strings (List[str]): List of strings to rank

        Returns:
            List[tuple]: List of (count, string) tuples sorted by count (descending)
        """
        ranked = [(self.count_keywords_in_string(s), s) for s in strings]
        return sorted(ranked, key=lambda x: x[0], reverse=True)

    def get_top_strings(self, strings: List[str], n: int = 5) -> List[str]:
        """
        Get the top n strings with the most synthesis keywords.

        Args:
            strings (List[str]): List of strings to filter
            n (int): Number of top strings to return

        Returns:
            List[str]: Top n strings with most keywords
        """
        ranked = self.rank_strings_by_relevance(strings)
        return [s for (count, s) in ranked[:n] if count > 0]