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
            suggestions = [
                "energy stocks slide in market",
                "stocks fall post price cuts",
                "surge in AI-focused companies",
                "CEO visit boosts stock price",
                "legacy automaker gains investor confidence",
                "crypto services see market rise",
                "Disney media stock soars",
                "electric vehicle chargers get upgrade",
                "energy stocks hit by oil prices",
                "AI-focused tech stock soars",
                "FDA accepts cancer treatment",
                "cybersecurity solutions get analyst upgrade",
                "semiconductor companies see mixed results",
                "Tesla stock impacted by short squeeze",
                "biotech company impacted by vaccine dose talks",
                "semiconductor giant faces earnings concerns",
                "tech company's quarterly performance",
                "positive reaction to software solutions",
                "computer company's earnings beat",
                "database software gets top pick status",
                "Fortinet reports earnings beat",
                "pharmacy chain sees leadership change",
                "mining company gets metals upgrade",
                "cloud services impacted by acquisition deal",
                "semiconductor company's market response"
            ]
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
                'vector': self.get_embedding(combined_text),
                'suggestions': suggestions
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
        start_time = time.time()
        params = {
            'defType': 'edismax',
            'q': input,
            'fq': 'doc_type:article',
            'fl': 'article_title article_link article_date article_text',
            'rows': rows
        }
        if from_date and to_date:
            params['fq'] += f" article_date:[{from_date} TO {to_date}]"
        elif from_date:
            params['fq'] += f" article_date:[{from_date} TO *]"
        elif to_date:
            params['fq'] += f" article_date:[* TO {to_date}]"
        if category:
            if params['fq'] != 'doc_type:article':
                params['fq'] += " AND"
            params['fq'] += " (article_keywords:" + category + " OR {!parent which='doc_type:article'}company_keywords:" + category + ")"
        boosts = {
            'article_title': 1,
            'article_text': 1,
            'article_keypoints': 1,
            'article_keywords': 1,
            'vector': 1
        }
        child_boosts = {
            'company_tag': 1,
            'company_name': 1,
            'company_description': 1,
            'company_keywords': 1
        }
        entities = self.analyzer.extract_entities(input)
        for entity in entities:
            if isinstance(entity, list) and len(entity) > 0:
                if isinstance(entity[0], list):
                    entity = entity[0]
                if len(entity) >= 2 and entity[1] == "NNP":
                    boosts['article_title'] += 4
                    boosts['article_keywords'] += 2
                    child_boosts['company_name'] += 2
                    child_boosts['company_tag'] += 1
                elif len(entity) >= 2 and entity[1] in ["NN", "NNS"]:
                    boosts['article_text'] += 3
                    boosts['article_keywords'] += 3
                    boosts['article_keypoints'] += 1
                    child_boosts['company_description'] += 1
                    child_boosts['company_keywords'] += 2
        for field in boosts:
            params['qf'] += f"{field}^{boosts[field]} "
        for field in child_boosts:
            params['bq'] = " {!parent which='doc_type:article'}" + field + "^" + child_boosts[field]
        if len(entities) >= 7:
            params['mm'] = '75%'
        results = self.query(params)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Query execution time: {elapsed_time} seconds")
        for param in params:
            print(f"{param}: {params[param]}")
        return results
    
# --------------------------------------------------------------------
    
    def configure_suggester(self):
        data = {
            "add-searchcomponent": {
                "name": "suggest",
                "class": "solr.SuggestComponent",
                "suggester": [
                    {
                        "name": "stock_suggester",
                        "lookupImpl": "FuzzyLookupFactory",
                        "dictionaryImpl": "DocumentDictionaryFactory",
                        "field": "suggestions",
                        "suggestAnalyzerFieldType": "stock_content"
                    }
                ]
            },
            "add-requesthandler": {
                "name": "/suggest",
                "class": "solr.SearchHandler",
                "startup": "lazy",
                "defaults": {
                    "suggest": True,
                    "suggest.dictionary": "stock_suggester",
                    "suggest.count": 10
                },
                "components": ["suggest"]
            }
        }
        url = f"{self.url}{self.core}/config"
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                print("Suggester configured successfully.")
            else:
                print(f"Failed to configure Suggester. Status code: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
    
    def suggest(self, input):
        try:
            params = {
                'suggest': 'true',
                'suggest.q': input,
                'suggest.dictionary': 'stock_suggester',
                'suggest.count': 5,
                'suggest.build': 'true'
            }
            url = f"{self.url}{self.core}/suggest"
            response = requests.get(url, params=params)
            if response.status_code == 200:
                suggestions = response.json()['suggest']['stock_suggester'][input]['suggestions']
                return suggestions
            else:
                print(f"Failed to retrieve suggestions. Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception occurred during suggestion retrieval: {str(e)}")
            return []

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
