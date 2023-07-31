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

        return self.analyze_positions(sorted_documents)

    def get_semantic_similarity(self, document):
        wp_similarities = []
        for document_synset in document["synsets"]:
            document_synset = wordnet.synset(document_synset)
            for interest_synset in self.user_interests:
                interest_synset = wordnet.synset(interest_synset)
                if document_synset.pos() == interest_synset.pos():
                    wp_similarity = interest_synset.wup_similarity(document_synset)
                    wp_similarities.append(wp_similarity)

        return self.get_document_average(wp_similarities)

    def get_document_average(self, similarity_scores):
        if len(similarity_scores) > 0:
            return sum(similarity_scores) / len(similarity_scores)

    def analyze_positions(self, documents):
        for index, document in enumerate(documents, start=1):
            document["new_position"] = index
            document["positions_difference"] = document["position"] - index
        return documents
