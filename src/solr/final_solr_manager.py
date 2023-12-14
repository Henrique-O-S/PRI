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
    def __init__(self, url ='http://localhost:8983/solr/', core = "articles", db_file = "sqlite:///../../data/articles.db"):
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
            time.sleep(3) # Wait for Solr core to start
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
        if sample == 0: sample = len(articles)
        for article in articles[:sample]:
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
            'q': '',
            'qf': '',
            'fq': 'doc_type:article',
            'bq': '',
            'fl': 'article_title article_link article_date article_text id',
            'rows': rows
        }
        if from_date and to_date:
            params['fq'] += f" article_date:[{from_date} TO {to_date}]"
        elif from_date:
            params['fq'] += f" article_date:[{from_date} TO *]"
        elif to_date:
            params['fq'] += f" article_date:[* TO {to_date}]"
        if from_date or to_date:
            params['sort'] = 'article_date desc'
        company_results = []
        unique_tags = set()
        boosts = {'article_title': 1, 'article_text': 1, 'article_keypoints': 1, 'article_keywords': 1, 'vector': 1}
        child_boosts = {'company_tag': 1, 'company_name': 1, 'company_description': 1, 'company_keywords': 1}
        entities = self.analyzer.extract_pos_tags(input)
        for entity in entities:
            word = entity[0]
            if word.islower():
                word = word.capitalize()
            if self.analyzer.is_org(word):
                results = self.company_query(word)
                for result in results:
                    company_tag = result.get('company_tag')
                    if company_tag not in unique_tags:
                        company_results.append(result)
                        unique_tags.add(company_tag)
                    break
                boosts['article_title'] += 9
                boosts['article_keywords'] += 6
                child_boosts['company_name'] += 3
                child_boosts['company_tag'] += 2
                params['q'] += str(entity[0]) + " "
            elif entity[1] == 'NOUN':
                boosts['article_text'] += 1
                boosts['article_keywords'] += 1
                child_boosts['company_description'] += 1
                child_boosts['company_keywords'] += 1
                params['q'] += str(entity[0]) + "~1 "
            else:
                params['q'] += str(entity[0]) + "~1 "
        if category:
            params['fq'] += " AND (article_keywords:" + category + " OR {!parent which='doc_type:article'}company_keywords:" + category + ")"
            results = self.sector_query(category)
            for result in results:
                company_tag = result.get('company_tag')
                if company_tag not in unique_tags:
                    company_results.append(result)
                    unique_tags.add(company_tag)
        for field in boosts:
            params['qf'] += f"{field}^{str(boosts[field])} "
        for field in child_boosts:
            params['bq'] += " {!parent which='doc_type:article'}" + field + "^" + str(child_boosts[field])
        if len(entities) >= 7:
            params['mm'] = '75%'
        if params['q'] == '':
            params['q'] = '*:*'
        results = self.query(params)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return {
            'results': results,
            'company_results': company_results,
            'params': params,
            'time': elapsed_time
        }
    
    def company_query(self, company):
        params = {
            'defType': 'edismax',
            'q': company,
            'qf': 'company_tag company_name',
            'fq': 'doc_type:company',
            'fl': 'company_name company_tag company_description',
            'rows': 1
        }
        results = self.query(params)
        return results
    
    def sector_query(self, sector):
        params = {
            'defType': 'edismax',
            'q': sector,
            'qf': 'company_keywords',
            'fq': 'doc_type:company',
            'fl': 'company_name company_tag company_description',
            'rows': 20,
        }
        results = self.query(params)
        return results
    
    def semantic_query(self, input, from_date = None, to_date = None, category = None, rows = 20):
        start_time = time.time()
        embedding = self.get_embedding(input)
        embedding = "[" + ",".join(map(str, embedding)) + "]"
        params = {
                'q': f"{{!knn f=vector topK=20}}{embedding}",
                'fl': 'article_title article_link article_date article_text',
                'fq': '',
                'rows': rows
        }
        if from_date and to_date:
            params['fq'] += f" article_date:[{from_date} TO {to_date}]"
        elif from_date:
            params['fq'] += f" article_date:[{from_date} TO *]"
        elif to_date:
            params['fq'] += f" article_date:[* TO {to_date}]"
        if from_date or to_date:
            params['sort'] = 'article_date desc'
        if category:
            params['fq'] += " AND (article_keywords:" + category + " OR {!parent which='doc_type:article'}company_keywords:" + category + ")"
        results = self.query(params)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return {
            'results': results,
            'params': params,
            'time': elapsed_time
        }
    
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
                response_json = response.json()['suggest']['stock_suggester'][input]['suggestions']
                suggestions = [suggestion['term'] for suggestion in response_json]
                return suggestions
            else:
                print(f"Failed to retrieve suggestions. Status code: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception occurred during suggestion retrieval: {str(e)}")
            return []
        
# --------------------------------------------------------------------

    def query_article(self, id):
        if not id:
            print("Please provide either id or content to find similar documents.")
            return []
        try:
            document = self.query({
                "q": f"id:{id}",
                "fq": "doc_type:article",
                "fl": "article_title article_link article_date article_text article_companies [child] company_name company_tag company_description",
                "rows": 1
            })
            if len(document) == 0:
                print(f"Document with ID {id} not found.")
                return []
        except Exception as e:
            print(f"An error occurred while fetching document: {str(e)}")
            return []
        return document
    
    def more_like_this(self, id=None, content=None, mltfl='article_text', rows=5):
        if not id and not content:
            print("Please provide either id or content to find similar documents.")
            return []
        if id:
            try:
                document = self.query({
                    "q": f"id:{id}",
                    "fq": "doc_type:article",
                    "rows": 1
                })
                if len(document) == 0:
                    print(f"Document with ID {id} not found.")
                    return []
                content = document.docs[0][mltfl]
            except Exception as e:
                print(f"An error occurred while fetching document: {str(e)}")
                return []
        content = content.replace(':', '')
        try:
            similar_docs = self.query({
                'q': mltfl + ':(' + content + ')',
                'fq': 'doc_type:article',
                'mlt': 'true',
                'mlt.fl': mltfl,
                'mlt.mindf': 1,
                'mlt.mintf': 1,
                'rows': rows
            })
            return similar_docs
        except Exception as e:
            print(f"An error occurred during More Like This query: {str(e)}")
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
