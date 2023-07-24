from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nltk.probability import FreqDist
from nltk import pos_tag
from re import sub
from nltk.stem import WordNetLemmatizer
from nltk.wsd import lesk


class Nlp:
    NUMBER_OF_KEYWORDS = 20

    def generate_keywords(self, text):
        tokens = self.remove_needless_words(text)
        keywords = self.filter_parts_of_speech(tokens)
        lemmas = self.lemmatize_terms(keywords)
        top_words = self.get_top_keywords(lemmas)

        synsets = []
        for word in top_words:
            word_sense = lesk(top_words, word, "n")
            try:
                synsets.append(word_sense.name())
            except:
                continue

        return [top_words, synsets]

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

    def lemmatize_terms(self, terms):
        lemmatizer = WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(word) for word in terms]
        return lemmas
