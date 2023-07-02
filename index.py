from flask import Flask, render_template, request, redirect, session
from app.solr_connector import SolrConnector
from app.web_crawler import WebCrawler
from app.database import User, init_database
from app.wordnets import Wordnets
import app.authentication as auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/search/')


@app.route("/search/", methods=['GET', 'POST'])
def search():
    auth = session.get('username')
    auth_user = User.query.filter_by(username=auth).first()
    if request.method == 'POST':
        query = request.form['query']

        solr_connector = SolrConnector()
        unsorted_results = solr_connector.searchByKeywords(query)

        wordnets = Wordnets(unsorted_results, auth_user.interests)
        sorted_results = wordnets.apply_recommendation_mechanism()

        searching_results = {
            'unsorted_results': unsorted_results,
            'sorted_results': sorted_results
        }
    users = User.query.all()
    return render_template('search.html', users=users, auth=auth, searching_results=searching_results)


@app.route("/crawl/", methods=['GET', 'POST'])
def crawl():
    if request.method == 'POST':
        url = request.form['url']

        web_crawler = WebCrawler()
        web_crawler.crawl(url)

    return render_template('crawl.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        redirect_route = '/' if auth.login(request) else 'login'
        return redirect(redirect_route)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        redirect_route = '/' if auth.register(request) else 'register'
        return redirect(redirect_route)

    return render_template('register.html')


@app.route('/logout')
def logout():
    auth.logout()
    return redirect('/')


if __name__ == "__main__":
    init_database(app)
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
