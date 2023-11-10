import pysolr
import json
import requests
import subprocess
import time
from Database import Database

class SolrManager:
    def __init__(self, url, core, db_file = "sqlite:///../../data/articles.db"):
        self.url = url
        self.core = core
        self.solr = None
        self.build()
        self.db = Database(db_file)

    def build(self):
        try:
            subprocess.run(["docker-compose", "up", "-d"], cwd="../")
            time.sleep(5)
            self.solr = pysolr.Solr(self.url + self.core, always_commit=True, timeout=10)
            print(f"Solr container with core {self.core} started successfully.")
        except Exception as e:
            print(f"Failed to start Solr container with core {self.core}: {str(e)}")

    def close(self):
        try:
            subprocess.run(["docker-compose", "down"], cwd="../")
            time.sleep(5)
            print(f"Solr container with core {self.core} stopped successfully.")
        except Exception as e:
            print(f"Failed to stop Solr container with core {self.core}: {str(e)}")

    def reload_core(self):
        try:
            unload_url = f"{self.url}admin/cores?action=UNLOAD&core={self.core}&deleteDataDir=true&deleteInstanceDir=true"
            response = requests.get(unload_url)
            if response.status_code == 200:
                print(f"Core {self.core} unloaded successfully.")
            else:
                print(f"Failed to unload core {self.core}. Status code: {response.status_code}")
                print(response.text)
                return
            self.close()
            self.build()
        except Exception as e:
            print(f"Failed to delete Solr core and data: {str(e)}")

    def clear_documents(self):
        clear_url = f"{self.url + self.core}/update?commit=true"
        data = '<delete><query>*:*</query></delete>'
        headers = {'Content-type': 'text/xml; charset=utf-8'}
        response = requests.post(clear_url, data=data, headers=headers)
        if response.status_code == 200:
            print("Data cleared successfully.")
        else:
            print(f"Failed to clear data. Status code: {response.status_code}")
            print(response.text)

    def submit_schema(self, schema_file_path):
        with open(schema_file_path, 'r') as schema_file:
            schema_json = json.load(schema_file)
        api_url = f"{self.url + self.core}/schema"
        headers = {'Content-type': 'application/json'}
        with open(schema_file_path, 'r') as schema_file:
            schema_json = schema_file.read()
        response = requests.post(api_url, data=schema_json, headers=headers)
        if response.status_code == 200:
            print("Schema uploaded successfully.")
        else:
            print(f"Failed to upload the schema. Status code: {response.status_code}")
            print(response.text)

    def apply_stopwords(self, stopwords_file):
        with open(stopwords_file, 'r') as file:
            stopwords = file.read()
        with open("../solr_data/data/articles/conf/stopwords.txt", 'w') as file:
            file.write(stopwords)
        print("Stopwords stored successfully.")

    def apply_synonyms(self, synonyms_file):
        with open(synonyms_file, 'r') as file:
            synonyms = file.read()
        with open("../solr_data/data/articles/conf/synonyms.txt", 'w') as file:
            file.write(synonyms)
        print("Synonyms stored successfully.")

    def index_articles(self):
        articles = self.db.get_all_articles()
        # test: indexing 10 articles
        counter = 10
        for article in articles:
            if counter == 0:
                break
            companies = self.db.get_article_companies(article.id)
            article_document = {  
                'id': article.id,
                'doc_type': 'article',
                'article_link': article.link,
                'article_title': article.title,
                'article_date': article.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'article_text': article.text,
                'article_keypoints': article.keypoints,
                'article_keywords': article.keywords,
                'article_companies': [
                    {
                        'doc_type': 'company',
                        'company_tag': company.tag,
                        'company_name': company.name,
                        'company_description': company.description,
                        'company_keywords': company.keywords
                    }
                    for company in companies
                ]
            }
            if len(article_document['article_companies']) == 1:
                article_document['article_companies'] = [article_document['article_companies']]
            print(f"Indexing article {article.id}...")
            self.solr.add([article_document])
            counter -= 1
        self.solr.commit()
        print("Articles indexed successfully.")

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