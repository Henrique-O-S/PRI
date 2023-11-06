from solr_manager import SolrManager

url = 'http://localhost:8983/solr/articles'
solr = SolrManager(url)

solr.create_schema("src/schema.json")
solr.index_articles()