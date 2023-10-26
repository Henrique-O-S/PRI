from indexer import Indexer

solr_url = 'http://localhost:8983/solr/gettingstarted'
solr_manager = Indexer(solr_url)
solr_manager.clear_data()
#solr_manager.index_articles()
solr_manager.index_companies()
