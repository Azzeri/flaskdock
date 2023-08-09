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
        keywords = query.split()
        query_string = " OR ".join(f"keywords:{keyword}" for keyword in keywords)

        searchResults = self.solr_instance.search(
            query_string,
            rows=self.no_results,
        )

        deduplicated = []
        encountered_titles = set()
        for result in searchResults:
            title = result["title"][0]
            if title not in encountered_titles:
                deduplicated.append(result)
                encountered_titles.add(title)

        preparedResults = []
        for index, result in enumerate(deduplicated, start=1):
            preparedResults.append(
                {
                    "id": result["id"],
                    "position": index,
                    "title": result["title"][0],
                    "keywords": result["keywords"],
                    "synsets": result["synsets"],
                }
            )

        # filtered_data = []
        # seen_names = set()

        # for item in preparedResults:
        #     title = item["title"][0]
        #     if title not in seen_names:
        #         filtered_data.append(item)
        #         seen_names.add(title)

        return preparedResults
