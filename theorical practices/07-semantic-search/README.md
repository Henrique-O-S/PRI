# Solr Semantic Search

Semantic Search refers to the ability of a system to understand the context and intent behind a user's query, rather than simply relying on keyword matching. Also known as "dense vector search," this method allows search systems to locate documents that share semantic relations with the query.

In this context, **dense vectors** differ from **sparse vectors** which are usually associated with inverted indexes. Sparse vectors have dimensions equal to the number of terms in the corpus, which often results in large vectors with most values being zeros.

Contrarily, dense vectors encapsulate semantic meaning into a confined number of dimensions. These dimensions can be significantly fewer than the terms in a corpus, allowing a more concise representation of the document's meaning.

To identify the closest dense vectors for a given query, a nearest neighbor search algorithm is used.

[Solr 9](https://solr.apache.org/guide/solr/9_4/query-guide/dense-vector-search.html) added support for the storage of dense vectors via the `DenseVectorField` type and dense vector matching through the `Knn Query Parser``.


## Semantic Search over M.EIC Courses

This tutorial aims to infuse semantic search capabilities into a search system designed for MEIC courses, previously described in [Solr 101: Running, Indexing, Retrieving](../05-solr).

The approach encompasses the following steps:

1. Use a deep learning model to derive embeddings for our documents.
2. Extend the existing Solr schema by incorporating a new field to store the document embeddings.
3. Run queries on the new collection utilizing Solr's nearest neighbor query parser.


## Generate Document Embeddings

For this purpose, we'll utilize the `sentence-transformers` library in Python and opt for the `all-MiniLM-L6-v2` model. The model stands out due to its compact size, yet it delivers quality on par with its larger counterparts (see [Using Sentence Transformers for semantic search](https://huggingface.co/spaces/sentence-transformers/embeddings-semantic-search)).

Ensure you have the sentence-transformers library installed:

```bash
pip install sentence-transformers
```

The script below expects a JSON file containing all the documents as its input. It then generates a new JSON document which includes a new `vector` field. This field is computed using the sentence-transformers library with the all-MiniLM-L6-v2 model, based on the `title`, `objectives`, and `learning_outcomes` fields.

```python
import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    # Read JSON from STDIN
    data = json.load(sys.stdin)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        title = document.get("title", "")
        objectives = document.get("objectives", "")
        learning_outcomes = document.get("learning_outcomes", "")

        combined_text = title + " " + objectives + " " + learning_outcomes
        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)
```

You can find the above script labeled as [get_embeddings.py](get_embeddings.py) in the repository.

To generate a new collection of documents complete with embeddings, use the command below:

```bash
cat meic_courses.json | python3 get_embeddings.py > semantic_courses.json
```


## Update Solr Schema to Store Document Embeddings

We need to modify the pre-existing Solr schema to incorporate a new field of the type `DenseVectorField`.

```json
{
    "add-field-type": [
        …,
        {
            "name": "courseVector",
            "class": "solr.DenseVectorField",
            "vectorDimension": 384,
            "similarityFunction": "cosine",
            "knnAlgorithm": "hnsw"
        }
    ],
    "add-field": [
        …,
        {
            "name": "vector",
            "type": "courseVector",
            "indexed": true,
            "stored": true
        }
    ]
}
```

You can access the complete schema, named [semantic_schema.json](semantic_schema.json), in the repository.

To initiate Solr with a fresh core, define the schema, and index the document collection, execute the following commands:

```bash
# Start Solr server with the current folder mapped to the container (at /data) and pre-create a core.
docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9.4 solr-precreate semantic_courses

# Add the schema defined at semantic_schema.json
curl -X POST -H 'Content-type:application/json' \
--data-binary "@./semantic_schema.json" \
http://localhost:8983/solr/semantic_courses/schema

# Index the JSON documents.
curl -X POST -H 'Content-type:application/json' \
--data-binary "@./semantic_courses.json" \
http://localhost:8983/solr/semantic_courses/update?commit=true
```

To inspect the vector field associated with each document, head to the Solr Dashboard at [http://localhost:8983].


## Semantic Querying with Dense Vector Embeddings 

To retrieve documents semantically similar to a given query, we'll leverage the dense vector embeddings. Due to the substantial size of these embeddings, POST requests are more apt for this task.

```python
import requests
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"

    data = {
        "q": f"{{!knn f=vector topK=10}}{embedding}",
        "fl": "id,title,score",
        "rows": 10,
        "wt": "json"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def display_results(results):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        print("No results found.")
        return

    for doc in docs:
        print(f"* {doc.get('id')} {doc.get('title')} [score: {doc.get('score'):.2f}]")

def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "semantic_courses"
    
    query_text = input("Enter your query: ")
    embedding = text_to_embedding(query_text)

    try:
        results = solr_knn_query(solr_endpoint, collection, embedding)
        display_results(results)
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()
```

The above script is saved as [query_embedding.py](query_embedding.py) in the repository.
