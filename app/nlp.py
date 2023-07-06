from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.probability import FreqDist
from nltk import pos_tag
from re import sub


class Nlp:
    NUMBER_OF_KEYWORDS = 15

    def generate_keywords(self, text):
        tokens = self.remove_needless_words(text)
        keywords = self.filter_parts_of_speech(tokens)
        return self.get_top_keywords(keywords)

    def remove_needless_words(self, text):
        text = BeautifulSoup(text, "html.parser").get_text()
        text = sub(r"[^\w\s]", "", text)
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        return [token.lower() for token in tokens if token.lower() not in stop_words]

    def filter_parts_of_speech(self, text):
        pos_tags = pos_tag(text)
        return [
            word for word, pos in pos_tags if pos.startswith("N") or pos.startswith("J")
        ]

    def get_top_keywords(self, keywords):
        freq_dist = FreqDist(keywords)
        return [
            keyword for keyword, _ in freq_dist.most_common(self.NUMBER_OF_KEYWORDS)
        ]
