from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from solr.final_solr_manager import SolrManager
import uvicorn
from datetime import datetime

db = 'sqlite:///../data/articles.db'
solr = SolrManager(db_file=db)

def init_solr():
    if 1: # Set to 0 to skip Solr initialization, if you have already initialized Solr
        print("Initializing Solr...")
        solr.reload_core()
        schema = 'solr/schema.json'
        print(f"Submitting schema {schema} to Solr...")
        solr.submit_schema(schema)
        print("Applying stopwords and synonyms...")
        solr.apply_stopwords('solr/stopwords.txt')
        solr.apply_synonyms('solr/synonyms.txt')
        solr.index_articles(400)
        print("Configuring suggester...")
        solr.configure_suggester()
        print("Done.")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# --------------------------------------------------------------------

@app.post("/predefined_query")
def post_predefined_query(item: dict):
    """
    Expects data in the following format:
    {
        "params": {...}
    }
    """
    if 'params' not in item:
        raise HTTPException(status_code=422, detail="The 'params' field is required.")
    
    params = item['params']
    results = solr.query(params)

    new_response = {
        'docs': results.docs,
        'hits': results.hits
    }
    results = new_response
    
    return {"response": results}

# --------------------------------------------------------------------

@app.post("/suggestions")
def post_suggestions(item: dict):
    """
    Expects data in the following format:
    {
        "text": "input"
    }
    """
    if 'text' not in item:
        raise HTTPException(status_code=422, detail="The 'text' field is required.")
    
    input= item['text']
    suggestions = solr.suggest(input)

    return {"response": suggestions}

# --------------------------------------------------------------------

@app.post("/user_query")
def post_query(item: dict):
    """
    Expects data in the following format:
    {
        "text": "input",
        "category": "category",               // can be ""
        "from_date": "YYYY-MM-DDTHH:MM:SSZ",  // can be ""
        "to_date": "YYYY-MM-DDTHH:MM:SSZ"     // can be ""
    }
    """
    if 'text' not in item or 'category' not in item:
        raise HTTPException(status_code=422, detail="The 'text' and 'category' fields are required.")
    
    if 'from_date' not in item or 'to_date' not in item:
        raise HTTPException(status_code=422, detail="The 'from_date' and 'to_date' fields are required.")
    
    input_text = item['text']
    input_category = item['category'] if item['category'] != "" else None
    input_from_date = item['from_date'] if item['from_date'] != "" else None
    input_to_date = item['to_date'] if item['to_date'] != "" else None

    date_format = "%Y-%m-%dT%H:%M:%SZ"
    if input_from_date:
        try:
            datetime.strptime(input_from_date, date_format)
        except ValueError:
            raise HTTPException(status_code=422, detail="Incorrect 'from_date' format, should be YYYY-MM-DDTHH:MM:SSZ")
        
    if input_to_date:
        try:
            datetime.strptime(input_to_date, date_format)
        except ValueError:
            raise HTTPException(status_code=422, detail="Incorrect 'to_date' format, should be YYYY-MM-DDTHH:MM:SSZ")
        
    # verify that from_date is before to_date
    if input_from_date and input_to_date:
        if datetime.strptime(input_from_date, date_format) >= datetime.strptime(input_to_date, date_format):
            raise HTTPException(status_code=422, detail="Incorrect date range, 'from_date' should be before 'to_date'")

    result = solr.user_query(input=input_text, category=input_category, from_date=input_from_date, to_date=input_to_date, rows=100)
    del result['params']

    if hasattr(result['results'], 'docs'):
        new_response = {
            'docs': result['results'].docs,
            'hits': result['results'].hits
        }
        result['results'] = new_response
    
    return {"response": result}

# --------------------------------------------------------------------

@app.post("/article_companies")
def post_query(item: dict):
    """
    Expects data in the following format:
    {
        "id": "article_id"
    }
    """
    if 'id' not in item:
        raise HTTPException(status_code=422, detail="The 'id' field is required.")
    
    input_id = item['id']

    result = solr.query_article(id=input_id)
    
    return {"response": result}

# --------------------------------------------------------------------

@app.post("/semantic_query")
def post_semantic_query(item: dict):
    """
    Expects data in the following format:
    {
        "text": "input",
        "category": "category",               // can be ""
        "from_date": "YYYY-MM-DDTHH:MM:SSZ",  // can be ""
        "to_date": "YYYY-MM-DDTHH:MM:SSZ"     // can be ""
    }
    """
    if 'text' not in item or 'category' not in item:
        raise HTTPException(status_code=422, detail="The 'text' and 'category' fields are required.")
    
    if 'from_date' not in item or 'to_date' not in item:
        raise HTTPException(status_code=422, detail="The 'from_date' and 'to_date' fields are required.")
    
    input_text = item['text']
    input_category = item['category'] if item['category'] != "" else None
    input_from_date = item['from_date'] if item['from_date'] != "" else None
    input_to_date = item['to_date'] if item['to_date'] != "" else None

    date_format = "%Y-%m-%dT%H:%M:%SZ"
    if input_from_date:
        try:
            datetime.strptime(input_from_date, date_format)
        except ValueError:
            raise HTTPException(status_code=422, detail="Incorrect 'from_date' format, should be YYYY-MM-DDTHH:MM:SSZ")
        
    if input_to_date:
        try:
            datetime.strptime(input_to_date, date_format)
        except ValueError:
            raise HTTPException(status_code=422, detail="Incorrect 'to_date' format, should be YYYY-MM-DDTHH:MM:SSZ")
        
    # verify that from_date is before to_date
    if input_from_date and input_to_date:
        if datetime.strptime(input_from_date, date_format) >= datetime.strptime(input_to_date, date_format):
            raise HTTPException(status_code=422, detail="Incorrect date range, 'from_date' should be before 'to_date'")

    result = solr.semantic_query(input=input_text, category=input_category, from_date=input_from_date, to_date=input_to_date)

    del result['params']

    if hasattr(result['results'], 'docs'):
        new_response = {
            'docs': result['results'].docs,
            'hits': result['results'].hits
        }
        result['results'] = new_response
    
    return {"response": result}

# --------------------------------------------------------------------

@app.post("/more_like_this")
def post_more_like_this(item: dict):
    """
    Expects data in the following format:
    {
        "id": "id",
        "content": "content",  // can be ""
    }
    """
    if 'id' not in item or 'content' not in item:
        raise HTTPException(status_code=422, detail="The 'id' and 'content' fields are required.")
    
    content = item['content'] if item['content'] != "" else None
    id = item['id']

    result = solr.more_like_this(id=id, content=content)

    if hasattr(result, 'docs'):
        for doc in result.docs:
            del doc['doc_type']
            del doc['id']
            del doc['article_text']
            del doc['article_keywords']
            del doc['article_date']
            del doc['article_link']
            del doc['vector']
            del doc['suggestions']
            del doc['_version_']

        new_response = {
            'docs': result.docs,
        }
        result = new_response
    
    return {"response": result}

# --------------------------------------------------------------------

if __name__ == "__main__":
    init_solr()
    uvicorn.run(app, port=8001)