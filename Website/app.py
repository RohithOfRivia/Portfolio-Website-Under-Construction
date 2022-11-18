from flask import Flask, render_template, url_for, request
from dotenv import load_dotenv
import scraper

import os


md = os.getenv('MD_KEY')

load_dotenv()

# instantiate the flask app
app = Flask(__name__)


# create each of the routes. The home page route
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


# about page route
@app.route("/about")
def about():
    return render_template('about.html')


# portfolio page route
@app.route("/portfolio", methods=['GET', 'POST'])
def portfolio():
    projects = [{"name": "kijiji Scraper", "desc": "Mining Project with python"}, {"name": "LA Crime Story", "desc": "used python and tableau"},
                {"name": "kijiji Scraper", "desc": "Mining Project with python"}, {"name": "LA Crime Story", "desc": "used python and tableau"},
                {"name": "kijiji Scraper", "desc": "Mining Project with python"}, {"name": "LA Crime Story", "desc": "used python and tableau"},
                {"name": "kijiji Scraper", "desc": "Mining Project with python"}, {"name": "LA Crime Story", "desc": "used python and tableau"}]
    return render_template('portfolio.html', projects=projects)


# contact me page route
@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/HousingScraper", methods=['GET', 'POST'])
def HousingScraper():

    if (request.method == 'POST'):

        if (request.form['scraper'] == 'start'):
            print("start recieved")
            # scraper.Stopper = False
            scraper.startScrape(scraper.startingLink, False)

        if (request.form['scraper'] == 'stop'):
            print("Stop recieved")
            scraper.Stopper = True
            scraper.startScrape(scraper.startingLink, True)
            # scraper.Stopper = True

    return render_template('HousingScraper.html')


if __name__ == "__main__":
    app.run(debug=True)