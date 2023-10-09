import nltk
import json
from nltk import word_tokenize, pos_tag, ne_chunk
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor

class Analyzer:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

    def extract_entities(self, text):
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        ner_result = ne_chunk(pos_tags)
        ner_json = json.dumps(ner_result)
        return ner_json

    def extract_keywords(self, text):
        blob = TextBlob(text)
        extractor = ConllExtractor()
        keywords = blob.noun_phrases
        keywords_json = json.dumps(keywords)
        return keywords_json
    