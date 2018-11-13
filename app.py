from flask import Flask, render_template, url_for

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#Database Setup
#must have "check_same_thread=False" or program will crash
engine = create_engine("sqlite:///DB/image.db?check_same_thread=False")
Base = automap_base()
Base.prepare(engine, reflect = True)
session = Session(engine)


#Set up Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB/image.db"
#added this to quiet the warnings. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Create variable for Table in DB
imageInfo=Base.classes.imageInfo

@app.route("/")
def index():
    
    results = session.query(imageInfo).all()
    
    print(type(results))
    # print(results[0]["ID"])
    print(type(results[0]))
    print(results[0].URL)
    # print(dir(results[0]))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)