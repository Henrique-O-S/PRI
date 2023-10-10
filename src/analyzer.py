import nltk
import json
from nltk import word_tokenize, pos_tag, ne_chunk
from textblob import TextBlob
import collections

class Analyzer:
    def __init__(self):
        nltk.download('brown')
        nltk.download('punkt')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

    def extract_entities(self, text):
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        ner_result = ne_chunk(pos_tags)
        ner_json = json.dumps(ner_result)
        return ner_json
    
    def extract_keywords(self, text, top_n=30):
        blob = TextBlob(text)
        noun_phrases = blob.noun_phrases
        noun_phrase_counts = collections.Counter(noun_phrases)
        sorted_noun_phrases = sorted(noun_phrase_counts.items(), key=lambda x: x[1], reverse=True)
        top_n_keywords = [phrase for phrase, _ in sorted_noun_phrases[:top_n]]
        keywords = ", ".join(top_n_keywords)
        return keywords
    