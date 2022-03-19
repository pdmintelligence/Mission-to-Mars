
#step 1 - use flask to render a template, redirecting to an URL and creating a URL
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#activating Flask*.
app = Flask(__name__)

#telling python to connect to Mongo using PyMongo.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# the code created will set up flask routes * 
#the return tells flask to rentrun an HTML template using an index.html file*.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)
#creating scraping route*. This route is the 'button' on the web application*.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()



