from bs4 import BeautifulSoup
from requests import get
from app.nlp import Nlp
from app.solr_connector import SolrConnector
from urllib.parse import urlparse


class WebCrawler:
    EN_LANGUAGE_SUFFIX = "en"

    def __init__(self):
        self.nlp = Nlp()

    def crawl_many(self, urls):
        for url in urls:
            try:
                self.crawl(url)
            except:
                continue

    def crawl(self, url):
        urls = []
        urls.append(url)

        response = get(url)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if parsed_url.scheme:
            domain = parsed_url.scheme + "://" + domain

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            if self.is_page_in_english(soup):
                for link in soup.find_all("a"):
                    href = link.get("href")

                    if href and href.startswith("/"):
                        extended_url = domain + href
                        if extended_url not in (urls):
                            urls.append(domain + href)

        self.index(urls)

    def index(self, urls):
        solr_connector = SolrConnector()
        solr = solr_connector.get_solr_instance()

        for url in urls:
            try:
                response = get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    keywords = self.nlp.generate_keywords(response.content)

                    document = {
                        "id": url,
                        "title": soup.title.string if soup.title else None,
                        "text": response.content,
                        "keywords": keywords[0],
                        "synsets": keywords[1],
                    }
                    solr.add(document)
            except:
                continue

    def extract_links(self, soup):
        links = soup.find_all("a")
        return [
            link.get("href")
            for link in links
            if link.get("href", "").startswith("https://")
        ]

    def save_to_solr(self, data):
        solr_connector = SolrConnector()
        solr = solr_connector.get_solr_instance()
        solr.add(data)

    def is_page_in_english(self, soup):
        page_language = self.get_page_language(soup)
        return page_language and page_language.startswith(self.EN_LANGUAGE_SUFFIX)

    def get_page_language(self, soup):
        html_element = soup.find("html")
        if html_element:
            return html_element.attrs.get("lang")
