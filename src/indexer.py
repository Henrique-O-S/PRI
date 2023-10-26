import pysolr
from Database import Database

class Indexer:
    def __init__(self, solr_url):
        self.solr = pysolr.Solr(solr_url, always_commit=True)
        self.db = Database()

    def index_articles(self):
        articles = self.db.get_all_articles()
        for article in articles:
            solr_document = {
                'id': article.id,
                'title': article.title,
                'date': article.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'text': article.text,
                'keypoints': article.keypoints,
                'keywords': article.keywords,
            }
            self.solr.add([solr_document])
        self.solr.commit()

    def index_companies(self):
        companies = self.db.get_all_companies()
        for company in companies:
            solr_document = {
                'id': company.id,
                'tag': company.tag,
                'name': company.name,
                'description': company.description,
                'keywords': company.keywords,
            }
            self.solr.add([solr_document])
        self.solr.commit()

    def clear_data(self):
        self.solr.delete(q='*:*')
        self.solr.commit()
