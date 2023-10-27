import pysolr
import json
import requests
from Database import Database

class Indexer:
    def __init__(self, solr_url):
        self.solr_url = solr_url
        self.solr = pysolr.Solr(self.solr_url, always_commit=True)
        self.db = Database()

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
