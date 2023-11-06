from indexer import Indexer

solr_url = 'http://localhost:8983/solr/articles'
solr_manager = Indexer(solr_url)

solr_manager.index_articles()
# solr_manager.index_companies()
#solr_manager.create_schema("src/schema.json")
