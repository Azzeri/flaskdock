from flask import Flask, render_template, request, redirect, url_for
from app.solr_connector import SolrConnector
from app.web_crawler import WebCrawler


app = Flask(__name__)


@app.route("/search/", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']

        solr_connector = SolrConnector()
        return solr_connector.searchByKeywords(query)
    return render_template('search.html')


@app.route("/crawl/", methods=['GET', 'POST'])
def crawl():
    if request.method == 'POST':
        url = request.form['url']

        web_crawler = WebCrawler()
        web_crawler.crawl(url)

    return render_template('crawl.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
