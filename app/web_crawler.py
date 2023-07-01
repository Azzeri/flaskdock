from bs4 import BeautifulSoup
from requests import get
from app.nlp import Nlp
from app.solr_connector import SolrConnector


class WebCrawler:

    EN_LANGUAGE_SUFFIX = 'en'

    def __init__(self):
        self.nlp = Nlp()

    def crawl(self, url, depth=1, max_pages=10):
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

                extracted_links = self.extract_links(soup)
                if extracted_links and depth < max_pages:
                    for link in extracted_links:
                        self.crawl(link, depth+1)

    def extract_links(self, soup):
        links = soup.find_all('a')
        return [link.get('href') for link in links if link.get('href', '').startswith('https://')]

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
