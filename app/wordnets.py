from nltk.corpus import wordnet
from statistics import mean
from itertools import chain
import json


class Wordnets:
    def __init__(self, search_results, user_interests):
        self.search_results = search_results
        self.user_interests = json.loads(user_interests)

    def apply_recommendation_mechanism(self):
        documents_with_semantic_similarity = []
        for document in self.search_results:
            semantic_similarity = self.get_semantic_similarity(document)
            document["semantic_similarity"] = semantic_similarity

            documents_with_semantic_similarity.append(document)
        sorted_documents = sorted(
            documents_with_semantic_similarity,
            key=lambda x: x["semantic_similarity"],
            reverse=True,
        )
        return sorted_documents

    def get_semantic_similarity(self, document):
        similarity_scores = []
        for keyword in document["keywords"]:
            keyword_synsets = wordnet.synsets(keyword)
            for interest in self.user_interests:
                interest_synsets = wordnet.synsets(interest)

                if self.synsets_exist(keyword_synsets, interest_synsets):
                    similarity_scores.append(
                        self.get_similarity_scores_for_every_synsets_pair(
                            keyword_synsets, interest_synsets
                        )
                    )

        return self.get_semantic_similarities_average(similarity_scores)

    def get_semantic_similarities_average(self, similarity_scores):
        if len(similarity_scores) > 0:
            return mean(list(chain(*similarity_scores)))

    def get_similarity_scores_for_every_synsets_pair(
        self, keyword_synsets, interest_synsets
    ):
        wp_similarities = []
        for keyword_synset in keyword_synsets:
            for interest_synset in interest_synsets:
                if keyword_synset.pos() == interest_synset.pos():
                    wp_similarity = interest_synset.wup_similarity(keyword_synset)
                    wp_similarities.append(wp_similarity)
        return wp_similarities

    def synsets_exist(self, keyword_synsets, interest_synsets):
        return len(keyword_synsets) > 0 and len(interest_synsets) > 0
