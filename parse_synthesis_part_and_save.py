from Article.ResearchArticle import ResearchArticle
from ExtractParts.CatalystSynthesisExtractor import CatalystSynthesisExtractor

if __name__ == "__main__":
    articles = ResearchArticle.from_csv('C:\\Users\\Aobo\\Desktop\\test.csv')
    extractor = CatalystSynthesisExtractor()

    for article in articles:
        article.load_paragraphs()
        article.load_synthesis_paragraphs(extractor)
        article.save_paragraphs_to_txt()
        print(article)
        print("---")