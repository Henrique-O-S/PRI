from fastapi import FastAPI, HTTPException
from solr.final_solr_manager import SolrManager
import uvicorn
from datetime import datetime

db = 'sqlite:///../data/articles.db'
solr = SolrManager(db_file=db)

def init_solr():
    if 1 == 0:
        print("Initializing Solr...")
        solr.reload_core()
        schema = 'solr/schema.json'
        print(f"Submitting schema {schema} to Solr...")
        solr.submit_schema(schema)
        print("Applying stopwords and synonyms...")
        solr.apply_stopwords('solr/stopwords.txt')
        solr.apply_synonyms('solr/synonyms.txt')
        solr.index_articles(100)
        print("Configuring suggester...")
        solr.configure_suggester()
        print("Done.")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/post")
def post_data(item: dict):
    # Process the data received in POST request
    return {"Received data": item}

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

@app.post("/user_query")
def post_query(item: dict):
    """
    Expects data in the following format:
    {
        "text": "input",
        "category": "category",     // can be ""
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

    result = solr.user_query(input=input_text, category=input_category, from_date=input_from_date, to_date=input_to_date)
    print(f"result parameters: {result['params']}")
    # delete params from result
    del result['params']
    return {"response": result}

if __name__ == "__main__":
    init_solr()
    uvicorn.run(app, port=8001)