import csv
from datetime import datetime
from typing import List, Optional

from DataHandler.DataService import DataService
from ExtractParts.CatalystSynthesisExtractor import CatalystSynthesisExtractor
from Parser.PDFParser import TextPDFParser
from Util.Util import Util
import os


class ResearchArticle:
    def __init__(self, **kwargs):
        # Initialize all possible attributes from the CSV columns
        self.Answers = []
        self.Reasonings = []
        self.Paragraphs = []
        self.Key = kwargs.get('Key')
        self.Item_Type = kwargs.get('Item Type')
        self.Publication_Year = kwargs.get('Publication Year')
        self.Author = kwargs.get('Author')
        self.Title = kwargs.get('Title')
        self.Publication_Title = kwargs.get('Publication Title')
        self.ISBN = kwargs.get('ISBN')
        self.ISSN = kwargs.get('ISSN')
        self.DOI = kwargs.get('DOI')
        self.Url = kwargs.get('Url')
        self.Abstract_Note = kwargs.get('Abstract Note')

        # Parser date fields
        self.Date = self._parse_date(kwargs.get('Date'))
        self.Date_Added = self._parse_datetime(kwargs.get('Date Added'))
        self.Date_Modified = self._parse_datetime(kwargs.get('Date Modified'))
        self.Access_Date = self._parse_datetime(kwargs.get('Access Date'))

        self.Pages = kwargs.get('Pages')
        self.Num_Pages = kwargs.get('Num Pages')
        self.Issue = kwargs.get('Issue')
        self.Volume = kwargs.get('Volume')
        self.Number_Of_Volumes = kwargs.get('Number Of Volumes')
        self.Journal_Abbreviation = kwargs.get('Journal Abbreviation')
        self.Short_Title = kwargs.get('Short Title')
        self.Series = kwargs.get('Series')
        self.Series_Number = kwargs.get('Series Number')
        self.Series_Text = kwargs.get('Series Text')
        self.Series_Title = kwargs.get('Series Title')
        self.Publisher = kwargs.get('Publisher')
        self.Place = kwargs.get('Place')
        self.Language = kwargs.get('Language')
        self.Rights = kwargs.get('Rights')
        self.Type = kwargs.get('Type')
        self.Archive = kwargs.get('Archive')
        self.Archive_Location = kwargs.get('Archive Location')
        self.Library_Catalog = kwargs.get('Library Catalog')
        self.Call_Number = kwargs.get('Call Number')
        self.Extra = kwargs.get('Extra')
        self.Notes = kwargs.get('Notes')
        self.File_Attachments = kwargs.get('File Attachments')
        self.Link_Attachments = kwargs.get('Link Attachments')
        self.Manual_Tags = kwargs.get('Manual Tags')
        self.Automatic_Tags = kwargs.get('Automatic Tags')
        self.TextPDFParser = TextPDFParser(self.File_Attachments)

        # And all the remaining fields...

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime.date]:
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None

    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[datetime]:
        if not datetime_str:
            return None
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def __repr__(self):
        return f"<ResearchArticle {self.Key}: {self.Title}>"

    @classmethod
    def from_csv(cls, file_path: str) -> List['ResearchArticle']:
        articles = []
        with open(file_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Clean empty strings and convert to None
                cleaned_row = {k: v if v != "" else None for k, v in row.items()}
                articles.append(cls(**cleaned_row))
        return articles

    def load_paragraphs(self):
        with self.TextPDFParser as parser:
            # Extract by paragraphs
            print("extracting paragraphs for paper: " + self.Title)
            paragraphs = parser.extract_paragraphs_as_text()
            self.Paragraphs = paragraphs

        parser.close()

    def load_synthesis_paragraphs(self, extractor: CatalystSynthesisExtractor):
        paragraphs = extractor.get_top_strings(self.Paragraphs)
        paragraphs = Util.filter_out_references(paragraphs)
        paragraphs = Util.filter_out_figure_captions(paragraphs)
        self.Paragraphs = paragraphs

    def save_paragraphs_to_txt(self):
        current_directory = os.getcwd()
        file_name = current_directory + '\\paragraphs\\' + Util.replace_slashes(self.DOI) + '.txt'
        Util.save_strings_to_file(self.Paragraphs, file_name)


# Example usage:
if __name__ == "__main__":
    articles = ResearchArticle.from_csv('C:\\Users\\Aobo\\Desktop\\test.csv')
    articles = articles[:3]
    for article in articles:
        article.load_paragraphs()
        print(article)
        print(f"Authors: {article.Author}")
        print(f"Published in: {article.Publication_Year}")
        print("---")
        print(article.Paragraphs)
        print("---")