#flask app imports
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
# import operator
# from __future__ import print_function
# from config import api_key
import urllib
#-----------------------------------------------------------------------

# Set to true if devloping on local machine. Turn to false when in production.
# This sets envronment variables to connect to API and database
developmentEnvironment = False
if developmentEnvironment == True:
    from config import api_key
    from config import dbURL
else:
    dbURL = os.environ.get('DATABASE_URL', '')
    api_key = os.environ.get('AZURE_API_KEY', '')

globalAzureResults= None
#Database Setup
#must have "check_same_thread=False" or program will crash

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

app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Connects to the database using the app config
db = SQLAlchemy(app)

#Create variable for Table in DB
image_info=Base.classes.image_info

#function to get AzureAPI info from url. Thi is only for URL addresses. It doesnt work for local file lookups. 
# Found from Microsoft github 
def azureAPI(urlAddress):
    _region = 'westus' #Here you enter the region of your subscription
    _url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)
    _key = api_key
    _maxNumRetries = 10

    def processRequest( json, data, headers, params ):
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
    params = { 'visualFeatures' : 'Color,Categories,Tags,Description,Faces,ImageType,Adult', 'details': 'Celebrities,Landmarks'}
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json' 
    json = { 'url': urlAddress } 
    data = None
    result = processRequest( json, data, headers, params )
    return result

#Use this function for azureAPI calls form local file
def azureAPIlocal(fp):
    print("here1")
    _region = 'westus' #Here you enter the region of your subscription
    _url = 'https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)
    _key = api_key
    _maxNumRetries = 10

    def processRequest( json, data, headers, params ):
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
        print(result)
        return result

    # Load raw image file into memory
    pathToFileInDisk = fp
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()
        
    # Computer Vision parameters
    params = { 'visualFeatures' : 'Color,Categories,Tags,Description,Faces,ImageType,Adult', 'details': 'Celebrities,Landmarks'}
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'
    json = None
    result = processRequest( json, data, headers, params )

    return result # returns json object

@app.route("/", methods=['GET', 'POST'])
def index():
    ## Not using
    #queries the imageInfo table and returns all results
            # results = session.query(image_info).all()
            # results1=results[0].id
            # print(type(results))
            # print(type(results[0]))
            #print the first row of the query and only the URL column
            # print(results[0].URL)
            # print(dir(results[0]))
    
    #Once Upload/Submit button is clicked the user sends a "Post" request

    # These variables must be set to none to start with in case the if statement is not executed
    azureResults= None
    sv = None
    imgPath= "static/FashionSanta.jpg"
    text = None

    if request.method == 'POST':
        global globalAzureResults
        # If they are send a file do this:
        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # sv= predict(filepath)
            imgPath= filepath
            sv= predict(imgPath, "local")
            azureResults=azureAPIlocal(imgPath)

            globalAzureResults= azureResults
            globalAzureResults= azureResults
            text = azureResults["description"]["captions"][0]["text"]

        # If they user is sending a URL do this:
        else:
            urlAddress = request.values.get("urlAddress")
            print(urlAddress)
            azureResults = azureAPI(urlAddress)
            imgPath=urlAddress
            sv=predict(imgPath, "url")

            globalAzureResults= azureResults
            text = azureResults["description"]["captions"][0]["text"]
            
    #Returns a variable "azureResults" to the HTML file. It is listed as {{azureResults}} in the HTML file
    return render_template("index.html",azureResults=azureResults, prediction=sv, predImg=imgPath, text=text)

# Use our ML model to Predict Santa or Not Santa
def predict(fp, source): #fp is "filepath" and source is either "url" or "local".
    # URL images must be saved to a local file first
    if source == "url":
        urllib.request.urlretrieve(fp, "static/uploads/file.jpg")
        fp= "static/uploads/file.jpg"
        
    #Load the image
    image = cv2.imread(fp)
    
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
    #format the label
    label = "{}: {:.2f}%".format(label, proba*100)

    #clear TF session or it will cause an issue upon refreshing page
    clear_session()
    
    return label

@app.route("/moreInfo")
def moreInfo():


    return render_template("index2.html",info =globalAzureResults)

#used to run the app
if __name__ == "__main__":
    app.run(debug=True)