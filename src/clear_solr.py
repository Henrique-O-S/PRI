from solr_manager import SolrManager

url = 'http://localhost:8983/solr/articles'
solr = SolrManager(url)

solr.clear_data()
solr.clear_schema()
