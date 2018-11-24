from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import os

#Image Analysis dependencies--------------------------------------------
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import imutils
import cv2
from keras.backend import clear_session
#-----------------------------------------------------------------------

#Database Setup
#must have "check_same_thread=False" or program will crash
engine = create_engine("sqlite:///DB/image.db?check_same_thread=False")
Base = automap_base()
Base.prepare(engine, reflect = True)
session = Session(engine)


#Set up Flask
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB/image.db"
#added this to quiet the warnings. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DATABASE_URL will contain the database connection string:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Connects to the database using the app config
db = SQLAlchemy(app)



#Create variable for Table in DB
# image_info=Base.classes.image_info

@app.route("/")
def index():
    
    #queries the imageInfo table and returns all results
    # results = session.query(imageInfo).all()
    
    # print(type(results))
    # print(type(results[0]))
    #print the first row of the query and only the URL column
    # print(results[0].URL)
    # print(dir(results[0]))

    return render_template("index.html")

@app.route("/predict")
def predict():
    #Use trained model to predict image

    #Load the image
    image = cv2.imread("image-classification-keras/image-classification-keras/examples/santa_02.jpg")
    orig = image.copy()

    #pre-process the image for classification
    #resize image to fit model shape
    image = cv2.resize(image, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    #load the trained convolutional neural network
    model = load_model("image-classification-keras/image-classification-keras/santa_not_santa.model")

    #classify the input image
    (notSanta, santa) = model.predict(image)[0]

    #build the label
    label = "Santa" if santa > notSanta else "Not Santa"
    proba = santa if santa > notSanta else notSanta
    label = "{}: {:.2f}%".format(label, proba*100)

    #draw the label on the image
    output = imutils.resize(orig, width=400)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)

    #clear TF session or it will cause an issue upon refreshing page
    clear_session()

    return render_template("index.html",label=label)

if __name__ == "__main__":
    app.run(debug=True)