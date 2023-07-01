from bs4 import BeautifulSoup
from requests import get
from app.nlp import Nlp
from app.solr_connector import SolrConnector


class WebCrawler:

    EN_LANGUAGE_SUFFIX = 'en'

    def __init__(self):
        self.nlp = Nlp()

    def crawl(self, url):
        response = get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            if self.is_page_in_english(soup):
                content = response.text
                description = soup.find('meta', attrs={'name': 'description'})
                keywords = self.nlp.generate_keywords(content)

                self.save_to_solr({
                    "id": url,
                    "title": soup.title.string if soup.title else None,
                    'description': description.get('content') if description else None,
                    'text': content,
                    "keywords": keywords
                })

    def save_to_solr(self, data):
        solr_connector = SolrConnector()
        solr = solr_connector.get_solr_instance()
        solr.add(data)

    def is_page_in_english(self, soup):
        page_language = self.get_page_language(soup)
        return page_language and page_language.startswith(self.EN_LANGUAGE_SUFFIX)

    def get_page_language(self, soup):
        html_element = soup.find('html')
        if html_element:
            return html_element.attrs.get('lang')
