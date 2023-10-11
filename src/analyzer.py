
import json
from nltk import word_tokenize, pos_tag, ne_chunk
from textblob import TextBlob
import collections
# import nltk

class Analyzer:
    """
    This class is used to extract entities and keywords from text.
    """
    def __init__(self):
        pass
        # The following lines are commented out because they are not needed for this part of the project
        # But will be used later on
        
        # Download necessary NLTK resources
        #nltk.download('brown')
        #nltk.download('punkt')
        #nltk.download('maxent_ne_chunker')
        #nltk.download('words')

    def extract_entities(self, text : str) -> str:
        """
        Extract entities from text.
        
        Parameters:
        - text: the text to extract entities from
        """

        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        ner_result = ne_chunk(pos_tags)
        ner_json = json.dumps(ner_result)
        return ner_json
    
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
    