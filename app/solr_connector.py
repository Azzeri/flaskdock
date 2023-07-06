from pysolr import Solr


class SolrConnector:
    def __init__(self):
        self.solr_core = "semantica"
        self.solr_port = 8983
        self.solr_url = f"http://solr:{self.solr_port}/solr/{self.solr_core}"
        self.solr_instance = self.get_solr_instance()

    def get_solr_instance(self):
        return Solr(self.solr_url, always_commit=True)

    def searchByKeywords(self, query):
        searchResults = self.solr_instance.search(f"keywords:{query}")
        preparedResults = []
        for result in searchResults:
            preparedResults.append(
                {
                    "id": result["id"],
                    "title": result["title"][0],
                    "keywords": result["keywords"],
                }
            )
        return preparedResults
