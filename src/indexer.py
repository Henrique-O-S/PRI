from elasticsearch import Elasticsearch
from Database import Database, Article, Company, CompanyArticleAssociation

class Indexer:
    def __init__(self):
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.database = Database()
        self.articles_index_name = "articles_index"
        self.companies_index_name = "companies_index"
        self.associations_index_name = "associations_index"

    def index_articles(self):
        articles = self.database.get_all_articles()
        for article in articles:
            doc_id = article.id
            document = {
                'title': article.title,
                'text': article.text,
                'date': article.date.strftime('%Y-%m-%d %H:%M:%S'),
                'keypoints': article.keypoints,
                'author': article.author,
                'keywords': article.keywords
            }
            self.es.index(index=self.articles_index_name, id=doc_id, body=document)
        print(f"Indexed {len(articles)} articles into Elasticsearch.")

    def index_companies(self):
        companies = self.database.get_all_companies()
        for company in companies:
            doc_id = company.id
            document = {
                'name': company.name,
                'description': company.description,
                'tag': company.tag,
                'keywords': company.keywords
            }
            self.es.index(index=self.companies_index_name, id=doc_id, body=document)
        print(f"Indexed {len(companies)} companies into Elasticsearch.")

    def index_associations(self):
        associations = self.database.get_all_company_article_associations()
        for association in associations:
            doc_id = f"{association.company_id}_{association.article_id}"
            document = {
                'company_id': association.company_id,
                'article_id': association.article_id
            }
            self.es.index(index=self.associations_index_name, id=doc_id, body=document)
        print(f"Indexed {len(associations)} associations into Elasticsearch.")

    def index_all(self):
        self.index_articles()
        self.index_companies()
        self.index_associations()
