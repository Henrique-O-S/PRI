import pysolr
import json
import requests
from Database import Database

class SolrManager:
    def __init__(self, solr_url, db_file = "sqlite:///data/articles.db"):
        self.solr_url = solr_url
        self.solr = pysolr.Solr(self.solr_url, always_commit=True, timeout=10)
        self.db = Database(db_file)

    def create_schema(self, schema_file_path):
        with open(schema_file_path, 'r') as schema_file:
            schema_json = json.load(schema_file)

        api_url = f"{self.solr_url}/schema"

        headers = {'Content-type': 'application/json'}
        with open(schema_file_path, 'r') as schema_file:
            schema_json = schema_file.read()
        response = requests.post(api_url, data=schema_json, headers=headers)

        if response.status_code == 200:
            print("Schema uploaded successfully.")
        else:
            print(f"Failed to upload the schema. Status code: {response.status_code}")
            print(response.text)

    def index_articles(self):
        articles = self.db.get_all_articles()
        # test: indexing 10 articles
        counter = 10
        for article in articles:
            if counter == 0:
                break
            document = {
                'title': article.title,
                'date': article.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'text': article.text,
                'keypoints': article.keypoints,
                'keywords': article.keywords
            }
            companies = self.db.get_article_companies(article.id) # TO DO: create this function in db
            document['companies'] = companies
            document['companies'] = [{
                    'tag': company.name,
                    'name': company.link,
                    'description': company.description,
                    'keywords': company.keywords
                } for company in companies]
            self.solr.add([document])
            counter -= 1
        self.solr.commit()

    def clear_data(self):
        self.solr_url = self.solr_url.rstrip('/')
        clear_url = f"{self.solr_url}/update?commit=true"
        data = '<delete><query>*:*</query></delete>'
        headers = {'Content-type': 'text/xml; charset=utf-8'}
        response = requests.post(clear_url, data=data, headers=headers)

        if response.status_code == 200:
            print("Data cleared successfully.")
        else:
            print(f"Failed to clear data. Status code: {response.status_code}")
            print(response.text)

    def clear_schema(self):
        api_url = f"{self.solr_url}/schema"
        response = requests.delete(api_url)

        if response.status_code == 200:
            print("Schema cleared successfully.")
        else:
            print(f"Failed to clear the schema. Status code: {response.status_code}")
            print(response.text)

    def query_articles(self, query_value = "*", query_fields = [], query_operator = ' OR ', return_fields = [], rows = 10):
        """
        The query must be of the type: 'field:value'.
        We can also use boolean operators like AND, OR, NOT. EX: 'field1:value1 AND field2:value2'
        The default query is '*:*' which returns all the documents.
        It is NOT possible to have a query like: "*:value", but "field:*" is possible.
        """

        if query_fields == []:
            query = str("*:" + ','.join(query_value))
        else:
            query = str(query_operator.join([f"{field}:{value}" for field, value in zip(query_fields, query_value)]))



        if return_fields == []:
            results = self.solr.search(query,**{
                'rows': rows,
            })
        else:
            results = self.solr.search(query, **{
                'rows': rows,
                'fl': ','.join(return_fields),
            })
        return results.docs