from indexer import Indexer

solr_url = 'http://localhost:8983/solr/articles'
solr_manager = Indexer(solr_url)

solr_manager.clear_data()
solr_manager.clear_schema()
