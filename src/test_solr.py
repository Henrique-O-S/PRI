from solr_manager import SolrManager

url = 'http://localhost:8983/solr/articles'
solr = SolrManager(url)

solr.index_articles()
# solr.create_schema("src/schema.json")
