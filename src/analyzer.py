
from textblob import TextBlob
import collections
import spacy

class Analyzer:
    """
    This class is used to extract entities and keywords from text.
    """
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        """
        IF IT DIES HERE, RUN THIS IN TERMINAL:
        python -m spacy download en_core_web_sm
        """

    def extract_pos_tags(self, text : str) -> str:
        """
        Extract entities from text.
        
        Parameters:
        - text: the text to extract entities from
        """

        doc = self.nlp(text)
        pos_tags = [(token.text, token.pos_) for token in doc]
        return pos_tags
    
    def is_org(self, term : str) -> bool:
        """
        Check if entity is an organization.

        Parameters:
        - term: the term to check
        """

        doc = self.nlp(term)
        if doc.ents:
            return doc.ents[0].label_ == "ORG"
        return False
    
    def extract_keywords(self, text : str, top_n : int = 30) -> str:
        """
        Extract keywords from text.

        Parameters:
        - text: the text to extract keywords from
        - top_n: the number of keywords to extract
        """

        blob = TextBlob(text)
        noun_phrases = blob.noun_phrases
        noun_phrase_counts = collections.Counter(noun_phrases)
        sorted_noun_phrases = sorted(noun_phrase_counts.items(), key=lambda x: x[1], reverse=True)
        top_n_keywords = [phrase for phrase, _ in sorted_noun_phrases[:top_n]]
        keywords = ", ".join(top_n_keywords)
        return keywords
    