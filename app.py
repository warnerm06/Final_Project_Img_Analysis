from flask import Flask, render_template, url_for, request
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
#Azure API Dependencies-------------------------------------------------
import time
import requests
import operator
# from __future__ import print_function
from config import api_key



#Database Setup
#must have "check_same_thread=False" or program will crash
# dbURL=os.environ.get('DATABASE_URL', '')
dbURL="postgres://oipdniwugjmahr:8da79ffe46a77f52d4b2bb4aecf0f63b948e5da73e4ddf9766ca5b07f1052d76@ec2-54-83-8-246.compute-1.amazonaws.com:5432/d5l81lr3nin6oj"

engine = create_engine(dbURL)
Base = automap_base()
Base.prepare(engine, reflect = True)
session = Session(engine)


#Set up Flask
app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB/image.db"

#added this to quiet the warnings. 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DATABASE_URL will contain the database connection string:
app.config['SQLALCHEMY_DATABASE_URI'] = dbURL
# conn = psycopg2.connect(DATABASE_URL, sslmode='require') #from heroku

app.config['UPLOAD_FOLDER'] = 'uploads'

# Connects to the database using the app config
db = SQLAlchemy(app)

#Create variable for Table in DB
image_info=Base.classes.image_info

def azureAPI(urlAddress):
    print("here1")
    _region = 'westus' #Here you enter the region of your subscription
    _url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)
    _key = api_key
    _maxNumRetries = 10

    def processRequest( json, data, headers, params ):
        print("Step1")
        retries = 0
        result = None

        while True:

            response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

            if response.status_code == 429: 

                print( "Message: %s" % ( response.json() ) )

                if retries <= _maxNumRetries: 
                    time.sleep(1) 
                    retries += 1
                    continue
                else: 
                    print( 'Error: failed after retrying!' )
                    break

            elif response.status_code == 200 or response.status_code == 201:

                if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                    result = None 
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                    if 'application/json' in response.headers['content-type'].lower(): 
                        result = response.json() if response.content else None 
                    elif 'image' in response.headers['content-type'].lower(): 
                        result = response.content
            else:
                print( "Error code: %d" % ( response.status_code ) )
                print( "Message: %s" % ( response.json() ) )

            break
            
        return result
    print("Step2")
    params = { 'visualFeatures' : 'Color,Categories,Tags,Description,Faces,ImageType,Adult', 'details': 'Celebrities,Landmarks'}

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json' 

    json = { 'url': urlAddress } 
    data = None

    result = processRequest( json, data, headers, params )
    print('Hello from Result', result)

    return result

@app.route("/", methods=['GET', 'POST'])
def index():
    
    #queries the imageInfo table and returns all results
    results = session.query(image_info).all()
    results1=results[0].id
    
    # print(type(results))
    # print(type(results[0]))
    #print the first row of the query and only the URL column
    # print(results[0].URL)
    # print(dir(results[0]))
    
    #Once Upload/Submit button is clicked the user sends a "Post" request
    azureResults= None
    if request.method == 'POST':
        # If they are send a file do this:
        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath) 

        # If they user is sending a URL do this:
        else:
            urlAddress = request.values.get("urlAddress")
            azureResults = azureAPI(urlAddress)

    return render_template("index.html",test=azureResults)

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
    

@app.route("/test/<urlAddress>")
def urlAddress():
    m=urlAddress
    return render_template("index.html",test=m)

if __name__ == "__main__":
    app.run(debug=True)