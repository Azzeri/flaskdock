from pysolr import Solr


class SolrConnector:
    def __init__(self):
        self.solr_core = "semantica"
        self.solr_port = 8983
        self.solr_url = f"http://solr:{self.solr_port}/solr/{self.solr_core}"
        self.solr_instance = self.get_solr_instance()
        self.no_results = 150

    def get_solr_instance(self):
        return Solr(self.solr_url, always_commit=True)

    def searchByKeywords(self, query):
        searchResults = self.solr_instance.search(
            f"keywords:{query}", rows=self.no_results
        )
        preparedResults = []
        for index, result in enumerate(searchResults, start=1):
            preparedResults.append(
                {
                    "id": result["id"],
                    "position": index,
                    "title": result["title"][0],
                    "keywords": result["keywords"],
                    "synsets": result["synsets"],
                }
            )
        return preparedResults
