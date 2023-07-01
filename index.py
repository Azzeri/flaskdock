from flask import Flask, render_template, request
from app.solr_connector import SolrConnector


app = Flask(__name__)


@app.route("/search/", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']

        solr_connector = SolrConnector()
        return solr_connector.searchByKeywords(query)
    return render_template('search.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
