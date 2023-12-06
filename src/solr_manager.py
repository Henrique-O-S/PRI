# --------------------------------------------------------------------

import pysolr
import json
import requests
import subprocess
import time
from sentence_transformers import SentenceTransformer
from Database import Database
from analyzer import Analyzer

# --------------------------------------------------------------------

class SolrManager:
    def __init__(self, url, core, db_file = "sqlite:///../../data/articles.db"):
        self.url = url
        self.core = core
        self.solr = None
        self.build()
        self.db = Database(db_file)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.analyzer = Analyzer()

# --------------------------------------------------------------------

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

# --------------------------------------------------------------------

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

# --------------------------------------------------------------------

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

# --------------------------------------------------------------------

    def get_embedding(self, text):
        return self.model.encode(text, convert_to_tensor=False).tolist()

    def index_articles(self, sample = 100):
        articles = self.db.get_all_articles()
        articles_to_index = [] 
        for article in articles:
            if sample == 0:
                break
            companies = self.db.get_article_companies(article.id)
            combined_text = article.text
            for company in companies:
                combined_text += " " + company.description
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
                ],
                'vector': self.get_embedding(combined_text)
            }
            if len(article_document['article_companies']) == 1:
                article_document['article_companies'] = [article_document['article_companies']]
            articles_to_index.append(article_document) 
            sample -= 1
        print(f"Indexing {len(articles_to_index)} articles...")
        self.solr.add(articles_to_index) 
        self.solr.commit()
        print("Articles indexed successfully.")

# --------------------------------------------------------------------

    def query(self, params):
        results = self.solr.search(**params)
        return results
    
    def user_query(self, input, from_date = None, to_date = None, category = None, rows = 20):
        params = {
            'defType': 'edismax',
            'q': input,
            'fq': 'doc_type:article',
            'qf': '',
            'fl': 'article_title article_link article_date article_text',
            'bf': 'recip(ms(NOW,article_date),1.65e-9,20,1)',
            'rows': rows
        }
        if from_date and to_date:
            params['fq'] += f" article_date:[{from_date} TO {to_date}]"
        elif from_date:
            params['fq'] += f" article_date:[{from_date} TO *]"
        elif to_date:
            params['fq'] += f" article_date:[* TO {to_date}]"
        if category:
            params['fq'] += " {!parent which='doc_type:article'}company_keywords:(" + category + ")^20" 
        fields = ""
        boosts = {
            'article_title': 1,
            'article_text': 1,
            'article_keypoints': 1,
            'article_keywords': 1,
            'vector': 1
        }
        entities = self.analyzer.extract_entities(input)
        for entity in entities:
            if isinstance(entity, list) and len(entity) > 0:
                if isinstance(entity[0], list):
                    entity = entity[0]
                if len(entity) >= 2 and entity[1] == "NNP":
                    boosts['article_title'] += 4
                    boosts['article_keywords'] += 2
                    params['fq'] += " {!parent which='doc_type:article'}company_name:(" + entity[0] + ")^2"
                    params['fq'] += " {!parent which='doc_type:article'}company_tag:(" + entity[0] + ")^1"
                elif len(entity) >= 2 and entity[1] in ["NN", "NNS"]:
                    boosts['article_text'] += 3
                    boosts['article_keywords'] += 3
                    boosts['article_keypoints'] += 1
                    params['fq'] += " {!parent which='doc_type:article'}company_description:(" + entity[0] + ")"
                    params['fq'] += " {!parent which='doc_type:article'}company_keywords:(" + entity[0] + ")"
        for field in boosts:
            fields += f"{field}^{boosts[field]} "
        params['qf'] = fields
        if len(entities) >= 7:
            params['mm'] = '75%'
        results = self.query(params)
        return results

# --------------------------------------------------------------------

    def write_text(self, file, text):
        lines = text.split('. ')
        combined_lines = []
        for line in lines:
            if combined_lines and combined_lines[-1] and combined_lines[-1][-1].isdigit() and line and line[0].isdigit():
                combined_lines[-1] += '. ' + line
            else:
                combined_lines.append(line)
        for line in combined_lines:
            file.write(line + '.\n')

# --------------------------------------------------------------------
