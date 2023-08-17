from flask import Flask, render_template, request, redirect, session, jsonify
from app.solr_connector import SolrConnector
from app.web_crawler import WebCrawler
from app.database import db
from app.user import User
from app.wordnets import Wordnets
import app.authentication as auth
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = "your_secret_key"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():
    return redirect("/search/")


@app.route("/search/", methods=["GET", "POST"])
def search():
    auth = session.get("username")
    auth_user = User.query.filter_by(username=auth).first()

    if request.method == "POST":
        query = request.form["query"]

        solr_connector = SolrConnector()
        unsorted_results = solr_connector.searchByKeywords(query)

        wordnets = Wordnets(unsorted_results[:18], auth_user.interests)
        sorted_results = wordnets.apply_recommendation_mechanism()

        searching_results = {
            "unsorted_results": unsorted_results[:18],
            "sorted_results": sorted_results[:18],
        }

        with open("logs/log.txt", "a") as file:
            file.write("\n-----PHASE-----\n")
            file.write("Query: " + query + "\n")
            file.write("User:" + auth_user.interests + "\n")
            file.write("Default:\n")
            json.dump(unsorted_results[:18], file)
            file.write("\n\nSorted:\n")
            json.dump(sorted_results[:18], file)

        return render_template(
            "search.html",
            auth=auth_user,
            searching_results=searching_results,
        )

    return render_template(
        "search.html", users=users, auth=auth_user, searching_results=None
    )


@app.route("/crawl/", methods=["GET", "POST"])
def crawl():
    if request.method == "POST":
        # url = request.form["url"]
        web_crawler = WebCrawler()
        # keywords = web_crawler.crawl(url)
        # return keywords
        urls = [
            # "https://en.wikipedia.org/wiki/Dog",
            # "https://www.mdpi.com/journal/animals",
            # "https://en.wikipedia.org/wiki/Animal",
            # "https://kids.nationalgeographic.com/animals",
            # "https://nationalzoo.si.edu/animals",
            # "https://a-z-animals.com/",
            # "https://www.trixie.de/en/productworld/terraristics",
            # "https://terraplaza.com/",
            # "https://en.wikipedia.org/wiki/Marine_life",
            # "https://oceana.org/marine-life/",
            # "https://www.noaa.gov/education/resource-collections/marine-life",
            # "https://genv.org/marine-life/",
            # "https://www.twinkl.pl/teaching-wiki/marine-life",
            # "https://www.marinebio.org/creatures/",
            # "https://www.britannica.com/science/ornithology",
            # "https://en.wikipedia.org/wiki/Ornithology",
            # "https://ornithology.com/",
            # "https://academic.oup.com/auk",
            # "https://www.springer.com/journal/10336",
            # "https://en.wikipedia.org/wiki/Hunting",
            # "https://en.wikipedia.org/wiki/Trophy_hunting",
            # "https://www.discoverwildlife.com/animal-facts/an-introduction-to-trophy-hunting/",
            # "https://www.hsi.org/issues/trophy-hunting/",
            # "https://www.humanesociety.org/all-our-fights/banning-trophy-hunting",
            # "https://www.spcai.org/take-action/trophy-hunting/trophy-hunting-defined",
            # "https://en.wikipedia.org/wiki/Cat",
            # "https://www.britannica.com/animal/cat",
            # "https://www.nationalgeographic.com/animals/mammals/facts/domestic-cat",
            # "https://www.understandinganimalresearch.org.uk/what-is-animal-research/a-z-animals/cat",
            # "https://en.wikipedia.org/wiki/Dog",
            # "https://www.britannica.com/animal/dog",
            # "https://www.nationalgeographic.com/animals/mammals/facts/domestic-dog",
            # "https://www.freepik.com/free-photos-vectors/dog-animal",
            # "https://animaldiversity.org/accounts/Canis_lupus_familiaris/",
            # "https://www.columbia.k12.oh.us/AnimalResearchReport.aspx",
            # "https://kids.nationalgeographic.com/animals/",
            # "https://www.nationalgeographic.com/",
            # "https://animalcorner.org/animals/",
            # "https://www.worldbookonline.com/wb/Login?ed=wb&tu=http%3A%2F%2Fwww.worldbookonline.com%2Fkids%2Fhome%3Bjsessionid%3DE9D007A8BCE9C43664AE7115663DA06F%3Fsubacct%3D&subacct=",
            # "https://animalfactguide.com/animal-facts/",
            # "https://www.softschools.com/facts/animals/",
            # "https://defenders.org/wildlife",
            # "https://nhpbs.org/natureworks/nw4.htm",
            # "https://nationalzoo.si.edu/animals/list",
            # "https://easyscienceforkids.com/animals-and-ecosystems/",
            # "https://www.ducksters.com/animals.php",
            # "https://www.brainpop.com/",
            # "https://en.wikipedia.org/wiki/Pet",
            # "https://www.twinkl.pl/resources/life-processes-and-living-things/animals/pets",
            # "https://wordwall.net/pl/community/pet-animals",
            # "https://www.britannica.com/animal/pet",
            # "https://en.wikipedia.org/wiki/Fishkeeping",
            # "https://www.fishkeeper.co.uk/help-and-advice",
            # "https://www.fishkeepingworld.com/",
            # "https://fishkeepingadvice.com/",
            # "https://en.wikipedia.org/wiki/Mammal",
            # "https://en.wikipedia.org/wiki/Bird",
            # "https://en.wikipedia.org/wiki/Monkey",
            # "https://en.wikipedia.org/wiki/Snake",
            # "https://en.wikipedia.org/wiki/Jellyfish",
            # "https://en.wikipedia.org/wiki/Sea_cucumber",
            # "https://en.wikipedia.org/wiki/Australonuphis",
            # "https://en.wikipedia.org/wiki/Eukaryote",
            # "https://en.wikipedia.org/wiki/Wojtek_(bear)",
            # "https://en.wikipedia.org/wiki/Coral",
            # "https://en.wikipedia.org/wiki/Juliane_Koepcke",
            # "https://en.wikipedia.org/wiki/XY_sex-determination_system",
            # "https://en.wikipedia.org/wiki/Mollusca",
            # "https://en.wikipedia.org/wiki/List_of_deadliest_animals_to_humans",
            # "https://en.wikipedia.org/wiki/Carl_Linnaeus",
            # "https://en.wikipedia.org/wiki/Lizard",
            # "https://en.wikipedia.org/wiki/Sea_urchin",
            # "https://en.wikipedia.org/wiki/Life",
            # "https://en.wikipedia.org/wiki/Cannibalism",
            # "https://en.wikipedia.org/wiki/List_of_animal_sounds",
            # "https://en.wikipedia.org/wiki/IUCN_Red_List",
            # "https://en.wikipedia.org/wiki/Sponge",
            # "https://en.wikipedia.org/wiki/Nematode",
            # "https://en.wikipedia.org/wiki/Turritopsis_dohrnii",
            # "https://en.wikipedia.org/wiki/Box_jellyfish",
            # "https://en.wikipedia.org/wiki/Leech",
            # "https://en.wikipedia.org/wiki/Starfish",
            # "https://en.wikipedia.org/wiki/Vertebrate",
            # "https://en.wikipedia.org/wiki/Mouse",
            # "https://en.wikipedia.org/wiki/Binomial_nomenclature",
            # "https://en.wikipedia.org/wiki/Fossil",
            # "https://en.wikipedia.org/wiki/Cnidaria",
            # "https://en.wikipedia.org/wiki/Largest_and_heaviest_animals",
            # "https://en.wikipedia.org/wiki/Earthworm",
            # "https://en.wikipedia.org/wiki/Invertebrate",
            # "https://en.wikipedia.org/wiki/Sea_anemone",
            # "https://en.wikipedia.org/wiki/Ctenophora",
            # "https://en.wikipedia.org/wiki/Nematomorpha",
            # "https://en.wikipedia.org/wiki/Albinism",
            # "https://en.wikipedia.org/wiki/List_of_animal_names",
            # "https://en.wikipedia.org/wiki/Arthropod",
            # "https://en.wikipedia.org/wiki/Tardigrade",
            # "https://en.wikipedia.org/wiki/Chordate",
            # "https://en.wikipedia.org/wiki/Human",
            # "https://en.wikipedia.org/wiki/Lists_of_animals",
            # "https://en.wikipedia.org/wiki/Prehistory",
            # "https://en.wikipedia.org/wiki/Paleontology",
            # "https://en.wikipedia.org/wiki/Spider",
            # "https://en.wikipedia.org/wiki/Scorpion",
            # "https://en.wikipedia.org/wiki/Lizard",
            # "https://en.wikipedia.org/wiki/Lion",
            # "https://en.wikipedia.org/wiki/Big_cat",
            # "https://en.wikipedia.org/wiki/List_of_largest_cats",
            # "https://en.wikipedia.org/wiki/British_big_cats",
            # "https://en.wikipedia.org/wiki/List_of_fictional_big_cats",
            # "https://en.wikipedia.org/wiki/Feline",
            # "https://en.wikipedia.org/wiki/Wolf",
            # "https://en.wikipedia.org/wiki/Canine",
            # "https://en.wikipedia.org/wiki/List_of_common_household_pests",
            # "https://en.wikipedia.org/wiki/List_of_animals_by_number_of_neurons",
            # "https://en.wikipedia.org/wiki/List_of_domesticated_animals",
            # "https://en.wikipedia.org/wiki/List_of_herbivorous_animals",
            # "https://en.wikipedia.org/wiki/Omnivore",
            # "https://en.wikipedia.org/wiki/Carnivore",
            # "https://en.wikipedia.org/wiki/Lists_of_extinct_species#Animals",
            # "https://en.wikipedia.org/wiki/List_of_extinct_bird_species_since_1500",
            # "https://en.wikipedia.org/wiki/List_of_recently_extinct_mammals",
            # "https://en.wikipedia.org/wiki/List_of_extinct_cetaceans",
            # "https://en.wikipedia.org/wiki/List_of_extinct_butterflies",
            # "https://en.wikipedia.org/wiki/Lists_of_amphibians_by_region",
            # "https://en.wikipedia.org/wiki/Lists_of_birds_by_region",
            # "https://en.wikipedia.org/wiki/Lists_of_mammals_by_region",
            # "https://en.wikipedia.org/wiki/Lists_of_reptiles_by_region",
            # "https://www.nationalgeographic.com/animals/topic/pets",
            # "https://www.nationalgeographic.com/animals/topic/facts-pictures",
            # "https://www.nationalgeographic.com/animals/topic/wildlife-watch",
            # "https://www.nationalgeographic.org/projects/photo-ark/",
            # "https://www.nationalgeographic.com/animals/topic/wild-cities",
            # "https://www.nationalgeographic.com/animals/article/invasive-hammerhead-worms",
            # "https://www.nationalgeographic.com/premium/article/camouflage-hidden-animals",
            # "https://www.nationalgeographic.com/premium/article/tick-bite-meat-allergy-spreading",
            # "https://www.nationalgeographic.com/animals/article/copperhead-snake-bites-venom",
            # "https://www.nationalgeographic.com/animals/article/dogs-functional-breeding-purebreds-shelters-rescues",
            # "https://www.nationalgeographic.com/animals",
            # "https://www.livescience.com/animals/whales/this-colossal-extinct-whale-was-the-heaviest-animal-to-ever-live",
            # "https://www.livescience.com/health/neuroscience/googles-mind-reading-ai-can-tell-what-music-you-listened-to-based-on-your-brain-signals",
            # "https://www.livescience.com/space/james-webb-telescope-discovers-giant-question-mark-galaxy-in-deep-space",
            # "https://www.livescience.com/animals",
            # "https://www.livescience.com/archaeology",
            # "https://www.livescience.com/planet-earth",
            # "https://www.livescience.com/physics-mathematics",
            # "https://www.livescience.com/animals/amphibians",
            # "https://www.livescience.com/animals/arachnids",
            # "https://www.livescience.com/animals/spiders/what-is-the-biggest-spider-in-the-world",
            # "https://www.livescience.com/animals/birds",
            # "https://www.livescience.com/animals/cnidaria",
            # "https://www.livescience.com/animals/crustaceans",
            # "https://www.livescience.com/animals/extinct-species",
            # "https://www.livescience.com/animals/fish",
            # "https://www.livescience.com/animals/insects",
            # "https://www.livescience.com/animals/land-mammals",
            # "https://www.livescience.com/animals/marine-mammals",
            # "https://www.livescience.com/animals/mollusks",
            # "https://www.livescience.com/animals/reptiles",
            # "https://www.sciencenews.org/topic/animals",
            # "https://www.sciencenews.org/all-stories",
            # "https://www.sciencenews.org/century",
            # "https://www.sciencenews.org/article/eight-bears-book-conservation",
            # "https://www.sciencenews.org/article/rats-wind-antennae-whiskers-eyes",
            # "https://www.popsci.com/category/animals/",
            # "https://www.popsci.com/category/insects/",
            # "https://www.popsci.com/category/cats/",
            # "https://www.popsci.com/category/bats/",
            # "https://www.popsci.com/category/endangered-species/",
            # "https://www.popsci.com/category/spiders/",
            # "https://www.popsci.com/category/whales/",
            # "https://www.popsci.com/category/fish/",
            # "https://www.popsci.com/category/bears/",
            # "https://www.popsci.com/category/dogs/",
            # "https://www.popsci.com/category/bees/",
            # "https://www.popsci.com/category/pets/",
            # "https://www.popsci.com/category/wildlife/",
            # "https://www.popsci.com/category/birds/",
            # "https://www.popsci.com/category/sharks/",
            # "https://www.nytimes.com/topic/subject/animals",
            # "https://www.smithsonianmag.com/tag/animals/",
            # "https://www.scientificamerican.com/animals/",
            # "https://www.newscientist.com/article-topic/animals/",
            # "https://www.nbcnews.com/animal-news",
            "https://en.wikipedia.org/wiki/Lists_of_fictional_animals",
            "https://en.wikipedia.org/wiki/List_of_individual_cats",
            "https://en.wikipedia.org/wiki/List_of_oldest_cats",
            "https://en.wikipedia.org/wiki/List_of_giant_squid_specimens_and_sightings",
            "https://en.wikipedia.org/wiki/List_of_individual_elephants",
            "https://en.wikipedia.org/wiki/List_of_historical_horses",
            "https://en.wikipedia.org/wiki/List_of_leading_Thoroughbred_racehorses",
            "https://en.wikipedia.org/wiki/List_of_individual_apes",
            "https://en.wikipedia.org/wiki/List_of_individual_bears",
            "https://en.wikipedia.org/wiki/List_of_giant_pandas",
            "https://en.wikipedia.org/wiki/List_of_individual_birds",
            "https://en.wikipedia.org/wiki/List_of_individual_bovines",
            "https://en.wikipedia.org/wiki/List_of_individual_cetaceans",
            "https://en.wikipedia.org/wiki/List_of_individual_dogs",
            "https://en.wikipedia.org/wiki/List_of_longest_living_dogs",
            "https://en.wikipedia.org/wiki/List_of_individual_monkeys",
            "https://en.wikipedia.org/wiki/List_of_individual_pigs",
            "https://en.wikipedia.org/wiki/List_of_wealthiest_animals",
            "https://en.wikipedia.org/wiki/List_of_fictional_bears",
            "https://en.wikipedia.org/wiki/List_of_fictional_birds",
            "https://en.wikipedia.org/wiki/List_of_fictional_felines",
            "https://en.wikipedia.org/wiki/List_of_fictional_pachyderms",
            "https://en.wikipedia.org/wiki/List_of_fictional_pigs",
            "https://en.wikipedia.org/wiki/Ape",
            "https://en.wikipedia.org/wiki/Gorilla",
            "https://en.wikipedia.org/wiki/Monkey",
            "https://en.wikipedia.org/wiki/Arachnid",
            "https://en.wikipedia.org/wiki/Scorpion",
            "https://en.wikipedia.org/wiki/Spider",
            "https://en.wikipedia.org/wiki/Bear",
            "https://en.wikipedia.org/wiki/Bird",
            "https://en.wikipedia.org/wiki/Chicken",
            "https://en.wikipedia.org/wiki/Eagle",
            "https://en.wikipedia.org/wiki/Owl",
            "https://en.wikipedia.org/wiki/Vulture",
            "https://en.wikipedia.org/wiki/Cat",
            "https://en.wikipedia.org/wiki/Cheetah",
            "https://en.wikipedia.org/wiki/Jaguar",
            "https://en.wikipedia.org/wiki/Lion",
            "https://en.wikipedia.org/wiki/Tiger",
            "https://en.wikipedia.org/wiki/Cattle",
            "https://en.wikipedia.org/wiki/Goat",
            "https://en.wikipedia.org/wiki/Dog",
            "https://en.wikipedia.org/wiki/Coyote",
            "https://en.wikipedia.org/wiki/Fox",
            "https://en.wikipedia.org/wiki/Dolphin",
            "https://en.wikipedia.org/wiki/Fish",
            "https://en.wikipedia.org/wiki/Eel",
            "https://en.wikipedia.org/wiki/Shark",
            "https://en.wikipedia.org/wiki/Insect",
            "https://en.wikipedia.org/wiki/Ant",
            "https://en.wikipedia.org/wiki/Caterpillar",
            "https://en.wikipedia.org/wiki/Butterfly",
            "https://en.wikipedia.org/wiki/Moth",
            "https://en.wikipedia.org/wiki/Marsupial",
            "https://en.wikipedia.org/wiki/Bandicoot",
            "https://en.wikipedia.org/wiki/Kangaroo",
            "https://en.wikipedia.org/wiki/Koala",
            "https://en.wikipedia.org/wiki/Opossum",
            "https://en.wikipedia.org/wiki/Tasmanian_devil",
            "https://en.wikipedia.org/wiki/Wallaby",
            "https://en.wikipedia.org/wiki/Wombat",
            "https://en.wikipedia.org/wiki/Mustelidae",
            "https://en.wikipedia.org/wiki/Badger",
            "https://en.wikipedia.org/wiki/Ferret",
            "https://en.wikipedia.org/wiki/Weasel",
            "https://en.wikipedia.org/wiki/Marten",
            "https://en.wikipedia.org/wiki/Wolverine",
            "https://en.wikipedia.org/wiki/Otter",
            "https://en.wikipedia.org/wiki/Octopus",
            "https://en.wikipedia.org/wiki/Pig",
            "https://en.wikipedia.org/wiki/Rabbit",
            "https://en.wikipedia.org/wiki/Reptile",
            "https://en.wikipedia.org/wiki/Lizard",
            "https://en.wikipedia.org/wiki/Snake",
            "https://en.wikipedia.org/wiki/Rodent",
            "https://en.wikipedia.org/wiki/Beaver",
            "https://en.wikipedia.org/wiki/Hamster",
            "https://en.wikipedia.org/wiki/Porcupine",
            "https://en.wikipedia.org/wiki/Rat",
            "https://en.wikipedia.org/wiki/Squirrel",
            "https://en.wikipedia.org/wiki/Skunk",
            "https://en.wikipedia.org/wiki/Snail",
            "https://en.wikipedia.org/wiki/Whale",
            "https://en.wikipedia.org/wiki/Worm",
            "https://en.wikipedia.org/wiki/Sponge",
            "https://en.wikipedia.org/wiki/Diploblasty",
            "https://en.wikipedia.org/wiki/ParaHoxozoa",
            "https://en.wikipedia.org/wiki/Bilateria",
            "https://en.wikipedia.org/wiki/Nephrozoa",
            "https://en.wikipedia.org/wiki/Ambulacraria",
            "https://en.wikipedia.org/wiki/Spiralia",
            "https://en.wikipedia.org/wiki/Mesozoa",
            "https://en.wikipedia.org/wiki/Platyzoa",
            "https://en.wikipedia.org/wiki/Lophotrochozoa",
            "https://en.wikipedia.org/wiki/List_of_reptiles",
            "https://en.wikipedia.org/wiki/List_of_fish_families",
            "https://en.wikipedia.org/wiki/List_of_amphibians",
            "https://en.wikipedia.org/wiki/List_of_ichthyosaur_genera",
            "https://en.wikipedia.org/wiki/List_of_pterosaur_genera",
            "https://en.wikipedia.org/wiki/List_of_plesiosaur_genera",
            "https://en.wikipedia.org/wiki/List_of_dinosaur_genera",
            "https://en.wikipedia.org/wiki/Lists_of_snakes",
            "https://en.wikipedia.org/wiki/Lists_of_snakes",
        ]
        # web_crawler.crawl(url)
        web_crawler.crawl_many(urls)

    return render_template("crawl.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        redirect_route = "/" if auth.login(request) else "login"
        return redirect(redirect_route)

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        redirect_route = "/" if auth.register(request) else "register"
        return redirect(redirect_route)

    return render_template("register.html")


@app.route("/logout")
def logout():
    auth.logout()
    return redirect("/")


@app.route("/users", methods=["GET"])
def users():
    users = User.query.all()

    return render_template("users.html", users=users)


@app.route("/mark/")
def mark():
    with open("logs/log.txt", "a") as file:
        file.write("\nRelevant result:\n")
        json.dump(request.args.get("result"), file)
        file.write(", Real position: " + request.args.get("real_position"))
        file.write(", Type: " + request.args.get("type"))
    return "ok"


@app.route("/like")
def like():
    synsets = request.args.get("synsets")

    auth = session.get("username")
    auth_user = db.session.query(User).filter_by(username=auth).first()
    auth_user.update_user_interests(synsets)

    with open("logs/log.txt", "a") as file:
        file.write("\nLiked result:\n")
        json.dump(request.args.get("result"), file)
        file.write(", Real position: " + request.args.get("real_position"))

    return jsonify(result=auth_user.interests)


@app.route("/analysis")
def analysis():
    from scipy import stats

    # Nienormalny
    q1_p1_g1 = [
        0.333333333,
        0.166666667,
        0.166666667,
        0.333333333,
        0.166666667,
        0.666666667,
        0.166666667,
    ]
    # Normalny
    q1_p1_g2 = [
        0.333333333,
        0.333333333,
        0,
        0.166666667,
        0.666666667,
        0.166666667,
        0.166666667,
    ]
    # Normalny
    q1_p1_g3 = [0.166666667, 0.666666667, 0.5, 0.333333333, 0.5, 0.5, 0.666666667]

    # Normalny
    q1_p2_g1 = [0.5, 0.333333333, 0.5, 0.333333333, 0.666666667, 0.666666667, 0.5]
    # Normalny
    q1_p2_g2 = [0.333333333, 0.5, 0, 0.166666667, 0.5, 0.666666667, 0.333333333]
    # Normalny
    q1_p2_g3 = [0, 0.333333333, 0.166666667, 0.333333333, 0.166666667, 0, 0.166666667]

    # statistic, p_value = stats.shapiro(q1_p1_g1)
    # return str(p_value)
    statistic, p_value = stats.ttest_rel(q1_p1_g3, q1_p2_g3)

    # Interpretacja wyników
    alpha = 0.05
    if p_value < alpha:
        return "Różnice są istotne statystycznie - odrzucamy hipotezę zerową."
    else:
        return "Nie ma istotnych różnic - nie odrzucamy hipotezy zerowej."

    # # Normalność
    # alpha = 0.05
    # if p_value < alpha:
    #     return "Rozkład danych nie jest normalny - odrzucamy hipotezę zerową."
    # else:
    #     return "Rozkład danych jest normalny - nie odrzucamy hipotezy zerowej."


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int("3000"), debug=True)
